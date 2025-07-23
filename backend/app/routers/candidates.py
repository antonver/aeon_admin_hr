from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database import get_db, Candidate, InterviewLog, Comment
from app.models import (
    CandidateCreate, CandidateUpdate, Candidate as CandidateModel,
    InterviewLogCreate, InterviewLog as InterviewLogModel,
    CommentCreate, Comment as CommentModel,
    CandidateFilter, QuickAction
)
from app.services.telegram_service import TelegramService
from app.services.notion_service import NotionService

router = APIRouter()

@router.get("/count")
async def get_candidates_count(
    search: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Candidate)
    if search:
        query = query.filter(Candidate.full_name.ilike(f"%{search}%"))
    if status:
        query = query.filter(Candidate.status == status)
    total = query.count()
    return {"total": total}

@router.get("/", response_model=List[CandidateModel])
async def get_candidates(
    search: Optional[str] = Query(None, description="Поиск по ФИО"),
    status: Optional[str] = Query(None, description="Фильтр по статусу"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Получить список кандидатов с фильтрацией"""
    query = db.query(Candidate)
    
    if search:
        query = query.filter(Candidate.full_name.ilike(f"%{search}%"))
    
    if status:
        query = query.filter(Candidate.status == status)
    
    candidates = query.offset(skip).limit(limit).all()
    return candidates

@router.post("/", response_model=CandidateModel)
async def create_candidate(
    candidate: CandidateCreate,
    db: Session = Depends(get_db)
):
    """Создать нового кандидата"""
    db_candidate = Candidate(**candidate.dict())
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    
    # Интеграция с Notion
    notion_service = NotionService()
    notion_id = await notion_service.create_candidate(db_candidate)
    db_candidate.notion_id = notion_id
    db.commit()
    
    return db_candidate

@router.get("/{candidate_id}", response_model=CandidateModel)
async def get_candidate(
    candidate_id: int,
    db: Session = Depends(get_db)
):
    """Получить кандидата по ID"""
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Кандидат не найден")
    return candidate

@router.put("/{candidate_id}", response_model=CandidateModel)
async def update_candidate(
    candidate_id: int,
    candidate_update: CandidateUpdate,
    db: Session = Depends(get_db)
):
    """Обновить кандидата"""
    db_candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not db_candidate:
        raise HTTPException(status_code=404, detail="Кандидат не найден")
    
    update_data = candidate_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_candidate, field, value)
    
    db_candidate.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_candidate)
    
    return db_candidate

@router.delete("/{candidate_id}")
async def delete_candidate(
    candidate_id: int,
    db: Session = Depends(get_db)
):
    """Удалить кандидата"""
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Кандидат не найден")
    
    db.delete(candidate)
    db.commit()
    return {"message": "Кандидат удален"}

# Интервью логи
@router.get("/{candidate_id}/interview-logs", response_model=List[InterviewLogModel])
async def get_interview_logs(
    candidate_id: int,
    db: Session = Depends(get_db)
):
    """Получить логи интервью кандидата"""
    logs = db.query(InterviewLog).filter(InterviewLog.candidate_id == candidate_id).all()
    return logs

@router.post("/{candidate_id}/interview-logs", response_model=InterviewLogModel)
async def create_interview_log(
    candidate_id: int,
    log: InterviewLogCreate,
    db: Session = Depends(get_db)
):
    """Создать лог интервью"""
    db_log = InterviewLog(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

# Комментарии HR
@router.get("/{candidate_id}/comments", response_model=List[CommentModel])
async def get_comments(
    candidate_id: int,
    db: Session = Depends(get_db)
):
    """Получить комментарии HR для кандидата"""
    comments = db.query(Comment).filter(Comment.candidate_id == candidate_id).all()
    return comments

@router.post("/{candidate_id}/comments", response_model=CommentModel)
async def create_comment(
    candidate_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db)
):
    """Создать комментарий HR"""
    db_comment = Comment(**comment.dict())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

# Быстрые действия
@router.post("/{candidate_id}/quick-action")
async def perform_quick_action(
    candidate_id: int,
    action: QuickAction,
    db: Session = Depends(get_db)
):
    """Выполнить быстрое действие с кандидатом"""
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Кандидат не найден")
    
    telegram_service = TelegramService()
    notion_service = NotionService()
    
    if action.action_type == "invite_test":
        # Отправить приглашение на тест
        await telegram_service.send_test_invitation(candidate)
        await notion_service.create_task(candidate, "Пригласить на тест")
        
    elif action.action_type == "telegram_message":
        # Отправить сообщение в Telegram
        message = action.data.get("message", "")
        await telegram_service.send_message(candidate, message)
        
    elif action.action_type == "send_feedback":
        # Отправить фидбэк
        feedback = action.data.get("feedback", "")
        await telegram_service.send_feedback(candidate, feedback)
        
    elif action.action_type == "copy_data":
        # Скопировать данные кандидата
        return {
            "full_name": candidate.full_name,
            "telegram": candidate.telegram_username,
            "email": candidate.email,
            "phone": candidate.phone
        }
    
    # Обновить последнее действие
    candidate.last_action_date = datetime.utcnow()
    candidate.last_action_type = action.action_type
    db.commit()
    
    return {"message": f"Действие {action.action_type} выполнено"} 

@router.post("/{candidate_id}/send-data")
async def send_candidate_data(
    candidate_id: int,
    format: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate or not candidate.telegram_username:
        raise HTTPException(status_code=404, detail="Кандидат не найден или нет Telegram")
    telegram_service = TelegramService()
    ok = await telegram_service.send_candidate_data_formatted(candidate, format)
    if ok:
        return {"message": "Данные отправлены кандидату в Telegram"}
    else:
        raise HTTPException(status_code=500, detail="Ошибка отправки данных в Telegram") 
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import Dict, Any
from datetime import datetime
import json

from backend.app.database import get_db, Candidate
from backend.app.services.telegram_service import TelegramService
from backend.app.services.notion_service import NotionService

router = APIRouter()

@router.post("/submit-results")
async def submit_interview_results(
    request: Request,
    db: Session = Depends(get_db)
):
    """Получить результаты интервью от внешнего сайта"""
    try:
        # Получаем данные из запроса
        body = await request.body()
        
        # Пытаемся парсить как JSON
        try:
            results = json.loads(body)
        except json.JSONDecodeError:
            # Если не JSON, пытаемся парсить как form data
            form_data = await request.form()
            results = dict(form_data)
        
        # Извлекаем данные из результатов
        full_name = results.get("full_name", "Неизвестный кандидат")
        telegram_username = results.get("telegram_username")
        telegram_id = results.get("telegram_id")
        interview_results = results.get("results", "")
        
        # Валидация обязательных полей
        if not full_name:
            raise HTTPException(status_code=400, detail="full_name обязателен")
        
        # Анализируем результаты и определяем статус
        def analyze_interview_results(results_text: str) -> str:
            if not results_text:
                return "ожидает"
            
            lower_results = results_text.lower()
            if "не берем" in lower_results:
                return "не берем"
            else:
                return "берем"
        
        # Определяем статус на основе результатов
        status = analyze_interview_results(interview_results)
        
        # Создаем нового кандидата
        candidate_data = {
            "full_name": full_name,
            "telegram_username": telegram_username,
            "telegram_id": telegram_id,
            "results": interview_results,
            "status": status
        }
        
        db_candidate = Candidate(**candidate_data)
        db.add(db_candidate)
        db.commit()
        db.refresh(db_candidate)
        
        # Интеграция с Notion
        try:
            notion_service = NotionService()
            notion_id = await notion_service.create_candidate(db_candidate)
            db_candidate.notion_id = notion_id
            db.commit()
        except Exception as e:
            print(f"Ошибка интеграции с Notion: {e}")
        
        # Отправляем уведомление администраторам
        try:
            telegram_service = TelegramService()
            await telegram_service.send_interview_completion_notification(db_candidate, 1, 0.0, db)
        except Exception as e:
            print(f"Ошибка отправки уведомления: {e}")
        
        return {
            "success": True,
            "message": "Результаты интервью успешно сохранены",
            "candidate_id": db_candidate.id,
            "status": status,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка сохранения результатов: {str(e)}")

@router.get("/results/{candidate_id}")
async def get_interview_results(
    candidate_id: int,
    db: Session = Depends(get_db)
):
    """Получить результаты интервью кандидата"""
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Кандидат не найден")
    
    return {
        "id": candidate.id,
        "full_name": candidate.full_name,
        "telegram_username": candidate.telegram_username,
        "results": candidate.results,
        "status": candidate.status,
        "created_at": candidate.created_at.isoformat() if candidate.created_at else None
    }

@router.options("/submit-results")
async def options_submit_results():
    """Обработчик OPTIONS для submit-results"""
    return {"message": "OK"}

@router.options("/results/{candidate_id}")
async def options_get_results(candidate_id: int):
    """Обработчик OPTIONS для get-results"""
    return {"message": "OK"}

@router.get("/health")
async def external_api_health():
    """Проверка здоровья внешнего API"""
    return {
        "status": "healthy",
        "service": "external-api",
        "timestamp": datetime.utcnow().isoformat()
    } 
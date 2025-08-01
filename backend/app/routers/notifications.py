from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime

from app.database import get_db, Notification, Candidate
from app.models import NotificationCreate, Notification as NotificationModel
from app.services.telegram_service import TelegramService
from app.services.notion_service import NotionService

router = APIRouter()

@router.get("/", response_model=List[NotificationModel])
async def get_notifications(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Получить список уведомлений"""
    notifications = db.query(Notification).offset(skip).limit(limit).all()
    return notifications

@router.post("/", response_model=NotificationModel)
async def create_notification(
    notification: NotificationCreate,
    db: Session = Depends(get_db)
):
    """Создать новое уведомление"""
    db_notification = Notification(**notification.dict())
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    
    # Отправить уведомления
    telegram_service = TelegramService()
    notion_service = NotionService()
    
    try:
        await telegram_service.send_notification(db_notification)
        db_notification.telegram_sent = True
    except Exception as e:
        print(f"Ошибка отправки в Telegram: {e}")
    
    try:
        await notion_service.create_notification_task(db_notification)
        db_notification.notion_sent = True
    except Exception as e:
        print(f"Ошибка отправки в Notion: {e}")
    
    db.commit()
    return db_notification

@router.get("/{notification_id}", response_model=NotificationModel)
async def get_notification(
    notification_id: int,
    db: Session = Depends(get_db)
):
    """Получить уведомление по ID"""
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Уведомление не найдено")
    return notification

@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db)
):
    """Удалить уведомление"""
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Уведомление не найдено")
    
    db.delete(notification)
    db.commit()
    return {"message": "Уведомление удалено"}

@router.post("/send-test")
async def send_test_notification():
    """Отправить тестовое уведомление"""
    telegram_service = TelegramService()
    notion_service = NotionService()
    
    try:
        await telegram_service.send_test_message()
        await notion_service.create_test_task()
        return {"message": "Тестовые уведомления отправлены"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка отправки: {str(e)}")

@router.post("/send-interview-notification/{candidate_id}")
async def send_interview_notification(
    candidate_id: int,
    db: Session = Depends(get_db)
):
    """Отправить уведомление о начале интервью"""
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Кандидат не найден")
    
    telegram_service = TelegramService()
    
    # Создаем уведомление в базе
    notification = Notification(
        candidate_id=candidate_id,
        type="interview_started",
        message=f"Кандидат {candidate.full_name} начал проходить интервью"
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    
    # Отправляем уведомление администраторам
    try:
        await telegram_service.send_interview_start_notification(candidate, db)
        notification.telegram_sent = True
        db.commit()
        return {"message": "Уведомление о начале интервью отправлено"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка отправки: {str(e)}")

@router.post("/send-status-change-notification/{candidate_id}")
async def send_status_change_notification(
    candidate_id: int,
    new_status: str,
    db: Session = Depends(get_db)
):
    """Отправить уведомление об изменении статуса кандидата"""
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Кандидат не найден")
    
    telegram_service = TelegramService()
    
    # Создаем уведомление в базе
    notification = Notification(
        candidate_id=candidate_id,
        type="status_changed",
        message=f"Статус кандидата {candidate.full_name} изменен на: {new_status}"
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    
    # Отправляем уведомление администраторам
    try:
        await telegram_service.send_status_change_notification(candidate, new_status, db)
        notification.telegram_sent = True
        db.commit()
        return {"message": "Уведомление об изменении статуса отправлено"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка отправки: {str(e)}")

@router.get("/stats")
async def get_notification_stats(db: Session = Depends(get_db)):
    """Получить статистику уведомлений"""
    total_notifications = db.query(Notification).count()
    telegram_sent = db.query(Notification).filter(Notification.telegram_sent == True).count()
    notion_sent = db.query(Notification).filter(Notification.notion_sent == True).count()
    
    # Статистика по типам
    type_stats = db.query(
        Notification.type,
        func.count(Notification.id).label('count')
    ).group_by(Notification.type).all()
    
    return {
        "total": total_notifications,
        "telegram_sent": telegram_sent,
        "notion_sent": notion_sent,
        "success_rate": (telegram_sent / total_notifications * 100) if total_notifications > 0 else 0,
        "type_stats": [{"type": stat.type, "count": stat.count} for stat in type_stats]
    } 
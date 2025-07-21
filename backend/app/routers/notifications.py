from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db, Notification
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
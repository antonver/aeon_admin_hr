from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.database import get_db, User
from backend.app.models import UserProfile, AdminCreateRequest
from backend.app.routers.telegram_auth import get_current_user_from_token
from typing import List
import logging

router = APIRouter()

@router.get("/admins", response_model=List[UserProfile])
async def get_admins(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """Получить список всех администраторов (только для админов)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    
    admins = db.query(User).filter(User.is_admin == True).all()
    
    return [
        UserProfile(
            id=admin.id,
            name=admin.name,
            email=admin.email,
            telegram_id=admin.telegram_id,
            telegram_username=admin.telegram_username,
            is_admin=admin.is_admin
        ) for admin in admins
    ]

@router.post("/admins")
async def create_admin(
    admin_request: AdminCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """Создать нового администратора (только для существующих админов)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    
    telegram_username = admin_request.telegram_username
    if not telegram_username:
        raise HTTPException(status_code=400, detail="Необходимо указать telegram_username")
    
    # Убираем @ если есть
    if telegram_username.startswith('@'):
        telegram_username = telegram_username[1:]
    
    # Ищем пользователя по username
    user = db.query(User).filter(User.telegram_username == telegram_username).first()
    if not user:
        raise HTTPException(
            status_code=404, 
            detail=f"Пользователь с username @{telegram_username} не найден. Пользователь должен сначала войти в приложение."
        )
    
    if user.is_admin:
        raise HTTPException(
            status_code=400, 
            detail=f"Пользователь @{user.telegram_username} уже является администратором"
        )
    
    user.is_admin = True
    db.commit()
    db.refresh(user)
    
    logging.info(f"Пользователь {user.name} (@{user.telegram_username}) назначен администратором")
    
    return {
        "message": f"Пользователь @{user.telegram_username} успешно назначен администратором",
        "user": UserProfile(
            id=user.id,
            name=user.name,
            email=user.email,
            telegram_id=user.telegram_id,
            telegram_username=user.telegram_username,
            is_admin=user.is_admin
        )
    }

@router.delete("/admins/{user_id}")
async def remove_admin(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """Удалить администратора (только для существующих админов)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    
    # Нельзя удалить самого себя
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Нельзя удалить самого себя из администраторов")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    if not user.is_admin:
        raise HTTPException(status_code=400, detail="Пользователь не является администратором")
    
    user.is_admin = False
    db.commit()
    db.refresh(user)
    
    logging.info(f"Пользователь {user.name} (@{user.telegram_username}) удален из администраторов")
    
    return {
        "message": f"Пользователь @{user.telegram_username} удален из администраторов",
        "user": UserProfile(
            id=user.id,
            name=user.name,
            email=user.email,
            telegram_id=user.telegram_id,
            telegram_username=user.telegram_username,
            is_admin=user.is_admin
        )
    } 
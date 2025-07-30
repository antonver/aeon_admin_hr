from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from app.database import get_db, User
from app.models import TelegramAuthRequest, UserProfile
from typing import Optional
import jwt
import os
import hashlib
import hmac
import urllib.parse
import logging
from telegram import Bot
import asyncio

router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY", "mysecret")
ALGORITHM = "HS256"
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

def validate_telegram_init_data(init_data: str) -> dict:
    """Валидация init_data от Telegram Mini Apps"""
    try:
        # Логируем входящие данные для отладки
        logging.info(f"Received init_data: {init_data}")
        
        if not init_data or init_data.strip() == "":
            raise HTTPException(status_code=400, detail="Пустые данные init_data")
        
        # Разбираем init_data
        parsed_data = urllib.parse.parse_qs(init_data)
        logging.info(f"Parsed data: {parsed_data}")
        
        # Извлекаем hash
        data_hash = parsed_data.get('hash', [None])[0]
        
        # Для тестирования пропускаем проверку подписи если BOT_TOKEN не настроен
        if BOT_TOKEN and data_hash:
            # Убираем hash из данных для проверки
            data_check_string = init_data.replace(f"&hash={data_hash}", "").replace(f"hash={data_hash}&", "").replace(f"hash={data_hash}", "")
            
            # Создаем секретный ключ
            secret_key = hmac.new(
                "WebAppData".encode(),
                BOT_TOKEN.encode(),
                hashlib.sha256
            ).digest()
            
            # Проверяем подпись
            calculated_hash = hmac.new(
                secret_key,
                data_check_string.encode(),
                hashlib.sha256
            ).hexdigest()
            
            if calculated_hash != data_hash:
                logging.error(f"Hash mismatch: expected {data_hash}, got {calculated_hash}")
                raise HTTPException(status_code=400, detail="Неверная подпись init_data")
        
        # Извлекаем данные пользователя
        user_data = {}
        for key, value in parsed_data.items():
            if key != 'hash':
                user_data[key] = value[0] if value else None
        
        # Если есть поле user, парсим его как JSON
        if 'user' in user_data and user_data['user']:
            try:
                import json
                user_json = json.loads(user_data['user'])
                user_data.update(user_json)
            except json.JSONDecodeError:
                logging.error(f"Ошибка парсинга JSON из user: {user_data['user']}")
        
        # Отладочная информация
        logging.info(f"Final user_data: {user_data}")
        
        return user_data
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Ошибка валидации init_data: {e}")
        raise HTTPException(status_code=400, detail="Неверный формат init_data")

def get_current_user_from_token(
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Требуется авторизация")
    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Неверный токен")
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        return user
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Неверный токен")

@router.post("/telegram-auth")
async def telegram_auth(
    auth_request: TelegramAuthRequest,
    db: Session = Depends(get_db)
):
    """Аутентификация через Telegram Mini Apps"""
    try:
        logging.info(f"Received auth request with init_data length: {len(auth_request.init_data) if auth_request.init_data else 0}")
        
        # Валидируем init_data
        user_data = validate_telegram_init_data(auth_request.init_data)
        
        # Извлекаем данные пользователя
        telegram_id = user_data.get('id')
        first_name = user_data.get('first_name', '')
        last_name = user_data.get('last_name', '')
        username = user_data.get('username')
        
        logging.info(f"Extracted user data: id={telegram_id}, name={first_name} {last_name}, username={username}")
        
        if not telegram_id:
            raise HTTPException(status_code=400, detail="ID пользователя не найден в init_data")
        
        # Ищем пользователя по telegram_id
        user = db.query(User).filter(User.telegram_id == str(telegram_id)).first()
        
        if not user:
            # Создаем нового пользователя
            user = User(
                name=f"{first_name} {last_name}".strip(),
                telegram_id=str(telegram_id),
                telegram_username=username,
                is_admin=False  # По умолчанию не админ
            )
            
            # Если это первый пользователь в системе, делаем его админом
            total_users = db.query(User).count()
            if total_users == 0:
                user.is_admin = True
                logging.info(f"Первый пользователь {telegram_id} назначен администратором")
            
            db.add(user)
            db.commit()
            db.refresh(user)
            logging.info(f"Создан новый пользователь: {user.name} (ID: {user.id})")
        else:
            # Обновляем данные существующего пользователя
            user.name = f"{first_name} {last_name}".strip()
            user.telegram_username = username
            db.commit()
            db.refresh(user)
            logging.info(f"Обновлен пользователь: {user.name} (ID: {user.id})")
        
        # Генерируем JWT токен
        token = jwt.encode(
            {"user_id": user.id, "is_admin": user.is_admin},
            SECRET_KEY,
            algorithm=ALGORITHM
        )
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": UserProfile(
                id=user.id,
                name=user.name,
                email=user.email,
                telegram_id=user.telegram_id,
                telegram_username=user.telegram_username,
                is_admin=user.is_admin
            )
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Ошибка аутентификации через Telegram: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

@router.get("/profile", response_model=UserProfile)
async def get_profile(user: User = Depends(get_current_user_from_token)):
    """Получить профиль текущего пользователя"""
    return UserProfile(
        id=user.id,
        name=user.name,
        email=user.email,
        telegram_id=user.telegram_id,
        telegram_username=user.telegram_username,
        is_admin=user.is_admin
    )

@router.post("/create-admin")
async def create_admin(
    admin_request: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """Создать нового администратора (только для существующих админов)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    
    telegram_username = admin_request.get('telegram_username')
    if not telegram_username:
        raise HTTPException(status_code=400, detail="Необходимо указать telegram_username")
    
    # Ищем пользователя по username
    user = db.query(User).filter(User.telegram_username == telegram_username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь с таким username не найден")
    
    if user.is_admin:
        raise HTTPException(status_code=400, detail="Пользователь уже является администратором")
    
    user.is_admin = True
    db.commit()
    db.refresh(user)
    
    logging.info(f"Пользователь {user.name} ({user.telegram_username}) назначен администратором")
    
    return {
        "message": "Администратор успешно создан",
        "user": UserProfile(
            id=user.id,
            name=user.name,
            email=user.email,
            telegram_id=user.telegram_id,
            telegram_username=user.telegram_username,
            is_admin=user.is_admin
        )
    }

@router.get("/admins")
async def get_admins(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """Получить список всех администраторов (только для админов)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    
    admins = db.query(User).filter(User.is_admin == True).all()
    
    return {
        "admins": [
            UserProfile(
                id=admin.id,
                name=admin.name,
                email=admin.email,
                telegram_id=admin.telegram_id,
                telegram_username=admin.telegram_username,
                is_admin=admin.is_admin
            ) for admin in admins
        ]
    } 
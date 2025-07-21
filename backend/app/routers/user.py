from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from app.database import get_db, User
from app.models import UserProfile, UserProfileUpdate
from typing import Optional
import jwt
import os
from pydantic import BaseModel
import bcrypt
import logging

router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY", "mysecret")
ALGORITHM = "HS256"

# Получить пользователя по токену из заголовка Authorization
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

@router.get("/profile", response_model=UserProfile)
async def get_profile(user: User = Depends(get_current_user_from_token)):
    return UserProfile(
        id=user.id,
        name=user.name,
        email=user.email
    )

@router.put("/profile", response_model=UserProfile)
async def update_profile(
    profile_update: UserProfileUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user_from_token)
):
    if profile_update.name:
        user.name = profile_update.name
    if profile_update.email:
        user.email = profile_update.email
    if profile_update.new_password:
        # Проверка текущего пароля
        if not profile_update.current_password or not bcrypt.checkpw(profile_update.current_password.encode(), user.password.encode()):
            raise HTTPException(status_code=400, detail="Неверный текущий пароль")
        user.password = bcrypt.hashpw(profile_update.new_password.encode(), bcrypt.gensalt()).decode()
    db.commit()
    db.refresh(user)
    return UserProfile(
        id=user.id,
        name=user.name,
        email=user.email
    )

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    logging.warning(f"LOGIN ATTEMPT: email={data.email}, password={data.password}, user_in_db={user.password if user else None}")
    if not user or not bcrypt.checkpw(data.password.encode(), user.password.encode()):
        raise HTTPException(status_code=401, detail="Неверный email или пароль")
    token = jwt.encode({"user_id": user.id}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"} 
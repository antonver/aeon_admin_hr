#!/usr/bin/env python3
"""
Инициализация базы данных для Docker/Heroku
Поддерживает как SQLite, так и PostgreSQL
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from app.database import Base, SessionLocal, User
from datetime import datetime

def init_db():
    """Инициализация базы данных"""
    print("🔧 Инициализация базы данных...")
    
    # Создаем таблицы
    Base.metadata.create_all(bind=engine)
    print("✅ Таблицы созданы")
    
    # Создаем тестового админа
    db = SessionLocal()
    try:
        # Проверяем, есть ли уже админ
        admin = db.query(User).filter(User.is_admin == True).first()
        if not admin:
            admin_user = User(
                name="Admin",
                email="admin@example.com",
                password="admin123",  # В продакшене используйте хеширование
                is_admin=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(admin_user)
            db.commit()
            print("✅ Тестовый админ создан")
            print("   Email: admin@example.com")
            print("   Пароль: admin123")
        else:
            print("ℹ️  Админ уже существует")
            
    except Exception as e:
        print(f"⚠️  Ошибка создания админа: {e}")
        db.rollback()
    finally:
        db.close()

def test_connection():
    """Тестирование подключения к базе данных"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Подключение к базе данных успешно")
            return True
    except Exception as e:
        print(f"❌ Ошибка подключения к базе данных: {e}")
        return False

if __name__ == "__main__":
    # Получаем URL базы данных из переменных окружения
    database_url = os.getenv("DATABASE_URL", "sqlite:///./hr_admin.db")
    
    # Для Heroku PostgreSQL
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    print(f"📊 Используется база данных: {database_url}")
    
    # Создаем движок
    engine = create_engine(database_url)
    
    # Тестируем подключение
    if not test_connection():
        sys.exit(1)
    
    # Инициализируем базу данных
    init_db()
    print("🎉 Инициализация завершена!") 
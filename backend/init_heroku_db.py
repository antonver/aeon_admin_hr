#!/usr/bin/env python3
"""
Скрипт для инициализации базы данных на Railway/Heroku
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import Base, engine, DATABASE_URL

load_dotenv()

def init_database():
    """Инициализация базы данных"""
    print("🔧 Инициализация базы данных...")
    
    try:
        # Проверяем подключение к базе данных
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Подключение к базе данных успешно")
            
        # Создаем все таблицы
        Base.metadata.create_all(bind=engine)
        print("✅ Таблицы созданы успешно")
        
        return True
        
    except OperationalError as e:
        print(f"❌ Ошибка подключения к базе данных: {e}")
        print(f"📊 DATABASE_URL: {DATABASE_URL}")
        return False
    except Exception as e:
        print(f"❌ Ошибка инициализации: {e}")
        return False

if __name__ == "__main__":
    success = init_database()
    if not success:
        sys.exit(1)
    print("🎉 База данных инициализирована успешно!") 
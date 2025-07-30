#!/usr/bin/env python3
"""
Скрипт для инициализации базы данных на Heroku
"""

import os
import sys
from dotenv import load_dotenv

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, Base, User
from sqlalchemy.orm import sessionmaker
import bcrypt

# Загружаем переменные окружения
load_dotenv()

def init_heroku_db():
    """Инициализация базы данных на Heroku"""
    try:
        # Создаем таблицы
        Base.metadata.create_all(bind=engine)
        print("✅ Таблицы созданы успешно")
        
        # Создаем сессию
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        try:
            # Проверяем, есть ли уже пользователи
            existing_users = db.query(User).count()
            
            if existing_users == 0:
                print("📝 Создаем первого администратора...")
                # Создаем тестового админа
                admin_user = User(
                    name="Heroku Admin",
                    email="admin@heroku.com",
                    password=bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()).decode(),
                    telegram_id="123456789",
                    telegram_username="heroku_admin",
                    is_admin=True
                )
                db.add(admin_user)
                db.commit()
                print("✅ Первый администратор создан:")
                print(f"   Email: admin@heroku.com")
                print(f"   Пароль: admin123")
                print(f"   Telegram ID: 123456789")
                print(f"   Telegram Username: heroku_admin")
            else:
                print(f"📊 В базе данных уже есть {existing_users} пользователей")
                
        except Exception as e:
            print(f"❌ Ошибка при создании пользователя: {e}")
            db.rollback()
        finally:
            db.close()
            
        print("🎉 База данных инициализирована успешно!")
        
    except Exception as e:
        print(f"❌ Ошибка инициализации базы данных: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_heroku_db() 
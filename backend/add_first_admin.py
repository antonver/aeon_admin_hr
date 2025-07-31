#!/usr/bin/env python3
"""
Скрипт для добавления первого администратора
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, User
from sqlalchemy.orm import Session

def add_first_admin():
    """Добавляет первого администратора AntonioDaVinchi"""
    db = SessionLocal()
    try:
        # Проверяем, есть ли уже пользователи в системе
        total_users = db.query(User).count()
        
        if total_users == 0:
            # Создаем первого админа
            admin = User(
                name="Antonio Da Vinci",
                telegram_username="AntonioDaVinchi",
                telegram_id="123456789",  # Временный ID для первого админа
                is_admin=True
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
            print(f"✅ Первый администратор создан:")
            print(f"   Имя: {admin.name}")
            print(f"   Username: @{admin.telegram_username}")
            print(f"   ID: {admin.id}")
            print(f"   Админ: {admin.is_admin}")
        else:
            # Ищем пользователя с username AntonioDaVinchi
            existing_admin = db.query(User).filter(User.telegram_username == "AntonioDaVinchi").first()
            
            if existing_admin:
                # Делаем его админом
                existing_admin.is_admin = True
                db.commit()
                print(f"✅ Пользователь @{existing_admin.telegram_username} назначен администратором")
            else:
                # Создаем нового админа
                admin = User(
                    name="Antonio Da Vinci",
                    telegram_username="AntonioDaVinchi",
                    telegram_id="123456789",  # Временный ID
                    is_admin=True
                )
                db.add(admin)
                db.commit()
                db.refresh(admin)
                print(f"✅ Администратор создан:")
                print(f"   Имя: {admin.name}")
                print(f"   Username: @{admin.telegram_username}")
                print(f"   ID: {admin.id}")
                print(f"   Админ: {admin.is_admin}")
        
        # Показываем всех админов
        admins = db.query(User).filter(User.is_admin == True).all()
        print(f"\n📋 Список администраторов ({len(admins)}):")
        for admin in admins:
            print(f"   - {admin.name} (@{admin.telegram_username})")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🔧 Добавление первого администратора...")
    add_first_admin()
    print("✅ Готово!") 
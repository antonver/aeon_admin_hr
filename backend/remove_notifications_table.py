#!/usr/bin/env python3
"""
Скрипт для удаления таблицы notifications из базы данных
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine
from sqlalchemy import text

def remove_notifications_table():
    """Удаляет таблицу notifications из базы данных"""
    db = SessionLocal()
    
    try:
        print("Удаляем таблицу notifications...")
        
        # Проверяем, существует ли таблица
        result = db.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='notifications'"))
        table_exists = result.fetchone()
        
        if table_exists:
            # Удаляем таблицу
            db.execute(text("DROP TABLE notifications"))
            db.commit()
            print("✅ Таблица notifications успешно удалена")
        else:
            print("ℹ️ Таблица notifications не существует")
        
        # Показываем список оставшихся таблиц
        result = db.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        tables = result.fetchall()
        
        print("\nОставшиеся таблицы в базе данных:")
        for table in tables:
            print(f"  - {table[0]}")
            
    except Exception as e:
        print(f"❌ Ошибка при удалении таблицы: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    remove_notifications_table() 
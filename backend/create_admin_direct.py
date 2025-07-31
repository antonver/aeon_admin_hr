#!/usr/bin/env python3
"""
Прямое создание администратора в базе данных
"""

import sqlite3
import os

def create_admin_direct():
    """Создает администратора напрямую в SQLite базе данных"""
    
    db_path = "hr_admin.db"
    
    if not os.path.exists(db_path):
        print(f"❌ База данных {db_path} не найдена")
        return
    
    try:
        # Подключаемся к базе данных
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Проверяем, есть ли таблица users
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if not cursor.fetchone():
            print("❌ Таблица users не найдена")
            return
        
        # Проверяем, есть ли уже админы
        cursor.execute("SELECT COUNT(*) FROM users WHERE is_admin = 1")
        admin_count = cursor.fetchone()[0]
        
        if admin_count == 0:
            # Создаем первого админа
            cursor.execute("""
                INSERT INTO users (name, telegram_username, telegram_id, is_admin, created_at, updated_at)
                VALUES (?, ?, ?, ?, datetime('now'), datetime('now'))
            """, ("Antonio Da Vinci", "AntonioDaVinchi", "123456789", True))
            
            conn.commit()
            print("✅ Первый администратор создан:")
            print("   Имя: Antonio Da Vinci")
            print("   Username: @AntonioDaVinchi")
            print("   ID: 123456789")
            print("   Админ: True")
        else:
            # Проверяем, есть ли уже пользователь с таким username
            cursor.execute("SELECT * FROM users WHERE telegram_username = ?", ("AntonioDaVinchi",))
            existing_user = cursor.fetchone()
            
            if existing_user:
                # Делаем его админом
                cursor.execute("UPDATE users SET is_admin = 1 WHERE telegram_username = ?", ("AntonioDaVinchi",))
                conn.commit()
                print("✅ Пользователь @AntonioDaVinchi назначен администратором")
            else:
                # Создаем нового админа
                cursor.execute("""
                    INSERT INTO users (name, telegram_username, telegram_id, is_admin, created_at, updated_at)
                    VALUES (?, ?, ?, ?, datetime('now'), datetime('now'))
                """, ("Antonio Da Vinci", "AntonioDaVinchi", "123456789", True))
                
                conn.commit()
                print("✅ Администратор создан:")
                print("   Имя: Antonio Da Vinci")
                print("   Username: @AntonioDaVinchi")
                print("   ID: 123456789")
                print("   Админ: True")
        
        # Показываем всех админов
        cursor.execute("SELECT name, telegram_username, is_admin FROM users WHERE is_admin = 1")
        admins = cursor.fetchall()
        
        print(f"\n📋 Список администраторов ({len(admins)}):")
        for admin in admins:
            print(f"   - {admin[0]} (@{admin[1]})")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    print("🔧 Прямое создание администратора...")
    create_admin_direct()
    print("✅ Готово!") 
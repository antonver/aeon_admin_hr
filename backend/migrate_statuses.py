#!/usr/bin/env python3
"""
Скрипт для миграции статусов кандидатов
Изменяет старые статусы на новые: "прошёл" -> "берем", "отклонён" -> "не берем"
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, Candidate
from sqlalchemy import text

def migrate_statuses():
    """Мигрирует статусы кандидатов"""
    db = SessionLocal()
    
    try:
        print("Начинаем миграцию статусов...")
        
        # Получаем всех кандидатов
        candidates = db.query(Candidate).all()
        
        updated_count = 0
        
        for candidate in candidates:
            old_status = candidate.status
            new_status = None
            
            # Определяем новый статус
            if old_status == "прошёл":
                new_status = "берем"
            elif old_status == "отклонён":
                new_status = "не берем"
            elif old_status == "приглашён":
                new_status = "берем"  # Приглашённые считаем как "берем"
            elif old_status in ["ожидает", "берем", "не берем"]:
                # Эти статусы уже в правильном формате
                continue
            else:
                # Неизвестный статус - оставляем как есть
                print(f"Неизвестный статус '{old_status}' для кандидата {candidate.id}")
                continue
            
            # Обновляем статус
            candidate.status = new_status
            updated_count += 1
            print(f"Кандидат {candidate.id} ({candidate.full_name}): {old_status} -> {new_status}")
        
        # Сохраняем изменения
        db.commit()
        
        print(f"\nМиграция завершена! Обновлено {updated_count} кандидатов.")
        
        # Показываем статистику
        from sqlalchemy import func
        status_counts = db.query(Candidate.status, func.count(Candidate.id)).group_by(Candidate.status).all()
        print("\nТекущее распределение статусов:")
        for status, count in status_counts:
            print(f"  {status}: {count}")
            
    except Exception as e:
        print(f"Ошибка при миграции: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    migrate_statuses() 
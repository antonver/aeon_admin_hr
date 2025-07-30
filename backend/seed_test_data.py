#!/usr/bin/env python3
"""
Скрипт для добавления тестовых кандидатов в базу данных
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import bcrypt
from app.database import SessionLocal, Candidate, InterviewLog, Comment, User
from datetime import datetime, timedelta
import random

def create_test_candidates():
    """Создает тестовых кандидатов с различными статусами и данными"""
    
    db = SessionLocal()
    
    # Тестовые данные кандидатов
    test_candidates = [
        {
            "full_name": "Иванов Иван Иванович",
            "telegram_username": "@ivan_dev",
            "telegram_id": "123456789",
            "results": "Хорошие результаты",
            "status": "ожидает"
        },
        {
            "full_name": "Петрова Анна Сергеевна",
            "telegram_username": "@anna_hr",
            "telegram_id": "234567890",
            "results": "Отличные результаты",
            "status": "приглашён"
        },
        {
            "full_name": "Сидоров Алексей Петрович",
            "telegram_username": "@alex_developer",
            "telegram_id": "345678901",
            "results": "Превосходные результаты",
            "status": "прошёл"
        },
        {
            "full_name": "Козлова Мария Дмитриевна",
            "telegram_username": "@maria_design",
            "telegram_id": "456789012",
            "results": "Средние результаты",
            "status": "отклонён"
        },
        {
            "full_name": "Волков Дмитрий Александрович",
            "telegram_username": "@dmitry_qa",
            "telegram_id": "567890123",
            "results": "Хорошие результаты",
            "status": "ожидает"
        },
        {
            "full_name": "Смирнова Елена Владимировна",
            "telegram_username": "@elena_manager",
            "telegram_id": "678901234",
            "results": "Отличные результаты",
            "status": "приглашён"
        },
        {
            "full_name": "Новиков Артём Игоревич",
            "telegram_username": "@artem_frontend",
            "telegram_id": "789012345",
            "results": "Превосходные результаты",
            "status": "прошёл"
        },
        {
            "full_name": "Морозова Кристина Андреевна",
            "telegram_username": "@kristina_analyst",
            "telegram_id": "890123456",
            "results": "Хорошие результаты",
            "status": "ожидает"
        },
        {
            "full_name": "Лебедев Сергей Николаевич",
            "telegram_username": "@sergey_backend",
            "telegram_id": "901234567",
            "results": "Отличные результаты",
            "status": "приглашён"
        },
        {
            "full_name": "Соколова Анастасия Павловна",
            "telegram_username": "@nastya_marketing",
            "telegram_id": "012345678",
            "results": "Превосходные результаты",
            "status": "прошёл"
        }
    ]
    
    # Дополнительные кандидаты для разных месяцев
    additional_candidates = [
        {
            "full_name": "Кузнецов Андрей Петрович",
            "telegram_username": "@andrey_dev",
            "telegram_id": "111111111",
            "results": "Хорошие результаты",
            "status": "прошёл"
        },
        {
            "full_name": "Иванова Ольга Сергеевна",
            "telegram_username": "@olga_hr",
            "telegram_id": "222222222",
            "results": "Отличные результаты",
            "status": "приглашён"
        },
        {
            "full_name": "Петров Михаил Александрович",
            "telegram_username": "@mikhail_qa",
            "telegram_id": "333333333",
            "results": "Средние результаты",
            "status": "отклонён"
        },
        {
            "full_name": "Сидорова Екатерина Дмитриевна",
            "telegram_username": "@ekaterina_design",
            "telegram_id": "444444444",
            "results": "Хорошие результаты",
            "status": "ожидает"
        },
        {
            "full_name": "Козлов Денис Игоревич",
            "telegram_username": "@denis_backend",
            "telegram_id": "555555555",
            "results": "Превосходные результаты",
            "status": "прошёл"
        }
    ]
    
    # Вопросы для интервью
    interview_questions = [
        {
            "question": "Расскажите о своем опыте работы с Python",
            "answer": "Работаю с Python уже 3 года, знаю Django, FastAPI, SQLAlchemy",
            "score": 8,
            "category": "навыки"
        },
        {
            "question": "Почему хотите работать в нашей компании?",
            "answer": "Интересные проекты, современные технологии, хорошая команда",
            "score": 9,
            "category": "мотивация"
        },
        {
            "question": "Как решаете конфликтные ситуации в команде?",
            "answer": "Стараюсь найти компромисс, выслушать все стороны",
            "score": 7,
            "category": "вовлечённость"
        },
        {
            "question": "Какие у вас есть слабые стороны?",
            "answer": "Иногда слишком перфекционист, но работаю над этим",
            "score": 8,
            "category": "честность"
        }
    ]
    
    # Комментарии HR
    hr_comments = [
        "Отличный кандидат, рекомендую к найму",
        "Нужно провести дополнительное интервью",
        "Подходит на позицию, но есть вопросы по опыту",
        "Очень мотивированный кандидат",
        "Требует дополнительного обучения"
    ]
    
    created_candidates = []
    
    try:
        # Создаем кандидатов для июля 2025
        for i, candidate_data in enumerate(test_candidates):
            # Добавляем случайную дату создания (последние 30 дней июля)
            days_ago = random.randint(0, 30)
            created_at = datetime(2025, 7, 1) + timedelta(days=days_ago)
            
            candidate = Candidate(
                **candidate_data,
                created_at=created_at,
                updated_at=created_at,
                last_action_date=created_at
            )
            
            db.add(candidate)
            db.commit()
            db.refresh(candidate)
            created_candidates.append(candidate)
            
            print(f"✅ Создан кандидат (июль): {candidate.full_name} (ID: {candidate.id})")
            
            # Добавляем логи интервью для некоторых кандидатов
            if candidate.status in ["прошёл", "приглашён"]:
                for j, question_data in enumerate(interview_questions):
                    if random.random() > 0.3:  # 70% вероятность добавления вопроса
                        interview_log = InterviewLog(
                            candidate_id=candidate.id,
                            **question_data,
                            created_at=created_at + timedelta(hours=j+1)
                        )
                        db.add(interview_log)
                
                # Добавляем комментарий HR
                comment = Comment(
                    candidate_id=candidate.id,
                    hr_comment=random.choice(hr_comments),
                    created_at=created_at + timedelta(hours=2)
                )
                db.add(comment)
            
            db.commit()
        
        # Создаем кандидатов для июня 2025
        for i, candidate_data in enumerate(additional_candidates[:3]):
            days_ago = random.randint(0, 30)
            created_at = datetime(2025, 6, 1) + timedelta(days=days_ago)
            
            candidate = Candidate(
                **candidate_data,
                created_at=created_at,
                updated_at=created_at,
                last_action_date=created_at
            )
            
            db.add(candidate)
            db.commit()
            db.refresh(candidate)
            created_candidates.append(candidate)
            
            print(f"✅ Создан кандидат (июнь): {candidate.full_name} (ID: {candidate.id})")
            
            # Добавляем логи интервью
            if candidate.status in ["прошёл", "приглашён"]:
                for j, question_data in enumerate(interview_questions):
                    if random.random() > 0.3:
                        interview_log = InterviewLog(
                            candidate_id=candidate.id,
                            **question_data,
                            created_at=created_at + timedelta(hours=j+1)
                        )
                        db.add(interview_log)
                
                comment = Comment(
                    candidate_id=candidate.id,
                    hr_comment=random.choice(hr_comments),
                    created_at=created_at + timedelta(hours=2)
                )
                db.add(comment)
            
            db.commit()
        
        # Создаем кандидатов для мая 2025
        for i, candidate_data in enumerate(additional_candidates[3:]):
            days_ago = random.randint(0, 30)
            created_at = datetime(2025, 5, 1) + timedelta(days=days_ago)
            
            candidate = Candidate(
                **candidate_data,
                created_at=created_at,
                updated_at=created_at,
                last_action_date=created_at
            )
            
            db.add(candidate)
            db.commit()
            db.refresh(candidate)
            created_candidates.append(candidate)
            
            print(f"✅ Создан кандидат (май): {candidate.full_name} (ID: {candidate.id})")
            
            # Добавляем логи интервью
            if candidate.status in ["прошёл", "приглашён"]:
                for j, question_data in enumerate(interview_questions):
                    if random.random() > 0.3:
                        interview_log = InterviewLog(
                            candidate_id=candidate.id,
                            **question_data,
                            created_at=created_at + timedelta(hours=j+1)
                        )
                        db.add(interview_log)
                
                comment = Comment(
                    candidate_id=candidate.id,
                    hr_comment=random.choice(hr_comments),
                    created_at=created_at + timedelta(hours=2)
                )
                db.add(comment)
            
            db.commit()
        
        print(f"\n🎉 Успешно создано {len(created_candidates)} тестовых кандидатов!")
        print("\n📊 Статистика по статусам:")
        
        # Показываем статистику
        statuses = db.query(Candidate.status).all()
        status_count = {}
        for status in statuses:
            status_count[status[0]] = status_count.get(status[0], 0) + 1
        
        for status, count in status_count.items():
            print(f"  • {status}: {count} кандидатов")
            
    except Exception as e:
        print(f"❌ Ошибка при создании тестовых данных: {e}")
        db.rollback()
    finally:
        db.close()


def create_admin_user():
    db = SessionLocal()
    email = "admin@example.com"
    password = "admin123"
    name = "Admin"
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    if not db.query(User).filter(User.email == email).first():
        user = User(name=name, email=email, password=hashed_password)
        db.add(user)
        db.commit()
        print(f"✅ Admin user created: {email} / {password}")
    else:
        print("Admin user already exists.")
    db.close()

if __name__ == "__main__":
    print("🚀 Создание тестовых кандидатов...")
    create_test_candidates()
    create_admin_user()
    print("\n✨ Готово! Теперь можно тестировать приложение.") 
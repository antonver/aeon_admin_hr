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
            "email": "ivan.ivanov@example.com",
            "phone": "+7 (999) 123-45-67",
            "status": "ожидает"
        },
        {
            "full_name": "Петрова Анна Сергеевна",
            "telegram_username": "@anna_hr",
            "email": "anna.petrova@example.com",
            "phone": "+7 (999) 234-56-78",
            "status": "приглашён"
        },
        {
            "full_name": "Сидоров Алексей Петрович",
            "telegram_username": "@alex_developer",
            "email": "alex.sidorov@example.com",
            "phone": "+7 (999) 345-67-89",
            "status": "прошёл"
        },
        {
            "full_name": "Козлова Мария Дмитриевна",
            "telegram_username": "@maria_design",
            "email": "maria.kozlova@example.com",
            "phone": "+7 (999) 456-78-90",
            "status": "отклонён"
        },
        {
            "full_name": "Волков Дмитрий Александрович",
            "telegram_username": "@dmitry_qa",
            "email": "dmitry.volkov@example.com",
            "phone": "+7 (999) 567-89-01",
            "status": "ожидает"
        },
        {
            "full_name": "Смирнова Елена Владимировна",
            "telegram_username": "@elena_manager",
            "email": "elena.smirnova@example.com",
            "phone": "+7 (999) 678-90-12",
            "status": "приглашён"
        },
        {
            "full_name": "Новиков Артём Игоревич",
            "telegram_username": "@artem_frontend",
            "email": "artem.novikov@example.com",
            "phone": "+7 (999) 789-01-23",
            "status": "прошёл"
        },
        {
            "full_name": "Морозова Кристина Андреевна",
            "telegram_username": "@kristina_analyst",
            "email": "kristina.morozova@example.com",
            "phone": "+7 (999) 890-12-34",
            "status": "ожидает"
        },
        {
            "full_name": "Лебедев Сергей Николаевич",
            "telegram_username": "@sergey_backend",
            "email": "sergey.lebedev@example.com",
            "phone": "+7 (999) 901-23-45",
            "status": "приглашён"
        },
        {
            "full_name": "Соколова Анастасия Павловна",
            "telegram_username": "@nastya_marketing",
            "email": "anastasia.sokolova@example.com",
            "phone": "+7 (999) 012-34-56",
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
        # Создаем кандидатов
        for i, candidate_data in enumerate(test_candidates):
            # Добавляем случайную дату создания (последние 30 дней)
            days_ago = random.randint(0, 30)
            created_at = datetime.utcnow() - timedelta(days=days_ago)
            
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
            
            print(f"✅ Создан кандидат: {candidate.full_name} (ID: {candidate.id})")
            
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
    # create_test_candidates()
    create_admin_user()
    print("\n✨ Готово! Теперь можно тестировать приложение.") 
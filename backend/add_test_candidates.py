from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, Candidate
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./hr_admin.db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def add_test_candidates():
    db = SessionLocal()
    
    # Проверяем, есть ли уже кандидаты
    existing_candidates = db.query(Candidate).count()
    if existing_candidates > 0:
        print(f"В базе уже есть {existing_candidates} кандидатов")
        return
    
    # Создаем тестовых кандидатов
    test_candidates = [
        {
            "full_name": "Иванов Иван Иванович",
            "name": "Иван",
            "telegram_username": "@ivan_test",
            "telegram_id": "123456789",
            "results": "Хорошие результаты тестирования",
            "status": "прошёл",
            "last_action_date": datetime.utcnow(),
            "last_action_type": "тестирование"
        },
        {
            "full_name": "Петрова Анна Сергеевна",
            "name": "Анна",
            "telegram_username": "@anna_test",
            "telegram_id": "987654321",
            "results": "Отличные результаты",
            "status": "прошёл",
            "last_action_date": datetime.utcnow(),
            "last_action_type": "интервью"
        },
        {
            "full_name": "Сидоров Алексей Петрович",
            "name": "Алексей",
            "telegram_username": "@alex_test",
            "telegram_id": "555666777",
            "results": "Не прошел тестирование",
            "status": "отклонён",
            "last_action_date": datetime.utcnow(),
            "last_action_type": "отклонение"
        },
        {
            "full_name": "Козлова Мария Дмитриевна",
            "name": "Мария",
            "telegram_username": "@maria_test",
            "telegram_id": "111222333",
            "results": "Средние результаты",
            "status": "отклонён",
            "last_action_date": datetime.utcnow(),
            "last_action_type": "отклонение"
        },
        {
            "full_name": "Волков Дмитрий Александрович",
            "name": "Дмитрий",
            "telegram_username": "@dmitry_test",
            "telegram_id": "444555666",
            "results": "Высокие результаты",
            "status": "прошёл",
            "last_action_date": datetime.utcnow(),
            "last_action_type": "принятие"
        }
    ]
    
    for candidate_data in test_candidates:
        candidate = Candidate(**candidate_data)
        db.add(candidate)
    
    db.commit()
    
    print(f"Добавлено {len(test_candidates)} тестовых кандидатов:")
    for i, candidate_data in enumerate(test_candidates, 1):
        print(f"{i}. {candidate_data['full_name']} - {candidate_data['status']}")
    
    db.close()

if __name__ == "__main__":
    add_test_candidates() 
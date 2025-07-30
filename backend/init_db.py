from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, User
import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./hr_admin.db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    # Создаем таблицы
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Проверяем, есть ли уже пользователи
    existing_user = db.query(User).first()
    if existing_user:
        print("Пользователи уже существуют в базе данных")
        return
    
    # Создаем тестового админа
    admin_password = "admin123"  # Простой пароль для тестирования
    hashed_password = bcrypt.hashpw(admin_password.encode(), bcrypt.gensalt()).decode()
    
    admin_user = User(
        name="Администратор",
        email="admin@example.com",
        password=hashed_password
    )
    
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    
    print(f"Тестовый админ создан:")
    print(f"Email: admin@example.com")
    print(f"Пароль: admin123")
    print(f"ID: {admin_user.id}")
    
    db.close()

if __name__ == "__main__":
    init_db() 
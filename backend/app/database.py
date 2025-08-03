from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./hr_admin.db")
# Для Heroku PostgreSQL
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Модели данных
class Candidate(Base):
    __tablename__ = "candidates"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    name = Column(String, nullable=True)  # Добавляем поле name
    telegram_username = Column(String, nullable=True)
    telegram_id = Column(String, nullable=True)
    results = Column(String, nullable=True)
    status = Column(String, default="ожидает")  # ожидает, берем, не берем
    last_action_date = Column(DateTime, default=datetime.utcnow)
    last_action_type = Column(String, nullable=True)
    notion_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Отношения
    interview_logs = relationship("InterviewLog", back_populates="candidate")
    comments = relationship("Comment", back_populates="candidate")

class InterviewLog(Base):
    __tablename__ = "interview_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    question = Column(String, nullable=False)
    answer = Column(Text, nullable=False)
    score = Column(Integer, nullable=True)  # 1-10
    category = Column(String, nullable=True)  # мотивация, вовлечённость, навыки, честность
    created_at = Column(DateTime, default=datetime.utcnow)
    
    candidate = relationship("Candidate", back_populates="interview_logs")

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    hr_comment = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    candidate = relationship("Candidate", back_populates="comments")

 

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True)  # может быть null для Telegram пользователей
    password = Column(String, nullable=True)  # может быть null для Telegram пользователей
    telegram_id = Column(String, unique=True, nullable=True)
    telegram_username = Column(String, nullable=True)
    is_admin = Column(Boolean, default=False)  # флаг администратора
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PendingAdmin(Base):
    __tablename__ = "pending_admins"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_username = Column(String, unique=True, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)  # кто добавил
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Отношение к пользователю, который добавил
    created_by_user = relationship("User") 
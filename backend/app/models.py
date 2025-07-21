from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Базовые модели
class CandidateBase(BaseModel):
    full_name: str
    telegram_username: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

class CandidateCreate(CandidateBase):
    pass

class CandidateUpdate(BaseModel):
    full_name: Optional[str] = None
    telegram_username: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    status: Optional[str] = None
    last_action_type: Optional[str] = None

class Candidate(CandidateBase):
    id: int
    status: str
    last_action_date: datetime
    last_action_type: Optional[str] = None
    notion_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Модели для интервью
class InterviewLogBase(BaseModel):
    question: str
    answer: str
    score: Optional[int] = None
    category: Optional[str] = None

class InterviewLogCreate(InterviewLogBase):
    candidate_id: int

class InterviewLog(InterviewLogBase):
    id: int
    candidate_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Модели для комментариев
class CommentBase(BaseModel):
    hr_comment: str

class CommentCreate(CommentBase):
    candidate_id: int

class Comment(CommentBase):
    id: int
    candidate_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Модели для уведомлений
class NotificationBase(BaseModel):
    type: str
    message: str

class NotificationCreate(NotificationBase):
    candidate_id: int

class Notification(NotificationBase):
    id: int
    candidate_id: int
    telegram_sent: bool
    notion_sent: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Модели для метрик
class Metrics(BaseModel):
    total_candidates: int
    active_candidates: int
    test_pass_rate: float
    weak_questions: List[str]

# Модели для фильтрации
class CandidateFilter(BaseModel):
    search: Optional[str] = None
    status: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None

# Модели для быстрых действий
class QuickAction(BaseModel):
    action_type: str  # invite_test, telegram_message, send_feedback, copy_data
    candidate_id: int
    data: Optional[dict] = None 

class UserProfile(BaseModel):
    id: int
    name: str
    email: str

class UserProfileUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    current_password: Optional[str] = None
    new_password: Optional[str] = None 
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List

from app.database import get_db, Candidate, InterviewLog
from app.models import Metrics

router = APIRouter()

@router.get("/overview", response_model=Metrics)
async def get_metrics_overview(db: Session = Depends(get_db)):
    """Получить общие метрики"""
    # Общее количество кандидатов
    total_candidates = db.query(Candidate).count()
    
    # Активные кандидаты (ожидают, прошёл, приглашён)
    active_candidates = db.query(Candidate).filter(
        Candidate.status.in_(["ожидает", "прошёл", "приглашён"])
    ).count()
    
    # Процент прохождения теста (кандидаты со статусом "прошёл")
    passed_candidates = db.query(Candidate).filter(Candidate.status == "прошёл").count()
    test_pass_rate = (passed_candidates / total_candidates * 100) if total_candidates > 0 else 0
    
   
    
    return Metrics(
        total_candidates=total_candidates,
        active_candidates=active_candidates,
        test_pass_rate=round(test_pass_rate, 2),
    )

@router.get("/status-distribution")
async def get_status_distribution(db: Session = Depends(get_db)):
    """Получить распределение по статусам"""
    status_counts = db.query(
        Candidate.status,
        func.count(Candidate.id).label('count')
    ).group_by(
        Candidate.status
    ).all()
    
    return {
        "distribution": [
            {"status": status, "count": count}
            for status, count in status_counts
        ]
    }

@router.get("/activity-timeline")
async def get_activity_timeline(
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Получить активность по дням"""
    from datetime import datetime, timedelta
    
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Активность по дням (последние действия)
    activity = db.query(
        func.date(Candidate.last_action_date).label('date'),
        func.count(Candidate.id).label('count')
    ).filter(
        Candidate.last_action_date >= start_date
    ).group_by(
        func.date(Candidate.last_action_date)
    ).order_by(
        func.date(Candidate.last_action_date)
    ).all()
    
    return {
        "timeline": [
            {"date": str(date), "count": count}
            for date, count in activity
        ]
    }

@router.get("/interview-stats")
async def get_interview_stats(db: Session = Depends(get_db)):
    """Получить статистику интервью"""
    # Средние баллы по категориям
    category_stats = db.query(
        InterviewLog.category,
        func.avg(InterviewLog.score).label('avg_score'),
        func.count(InterviewLog.id).label('count')
    ).filter(
        InterviewLog.score.isnot(None),
        InterviewLog.category.isnot(None)
    ).group_by(
        InterviewLog.category
    ).all()
    
    return {
        "category_stats": [
            {
                "category": stat.category,
                "avg_score": round(float(stat.avg_score), 2),
                "count": stat.count
            }
            for stat in category_stats
        ]
    }

@router.get("/top-candidates")
async def get_top_candidates(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Получить топ кандидатов по среднему баллу"""
    top_candidates = db.query(
        Candidate.full_name,
        func.avg(InterviewLog.score).label('avg_score'),
        func.count(InterviewLog.id).label('questions_count')
    ).join(
        InterviewLog, Candidate.id == InterviewLog.candidate_id
    ).filter(
        InterviewLog.score.isnot(None)
    ).group_by(
        Candidate.id, Candidate.full_name
    ).having(
        func.count(InterviewLog.id) >= 3  # Минимум 3 вопроса
    ).order_by(
        desc(func.avg(InterviewLog.score))
    ).limit(limit).all()
    
    return {
        "top_candidates": [
            {
                "full_name": candidate.full_name,
                "avg_score": round(float(candidate.avg_score), 2),
                "questions_count": candidate.questions_count
            }
            for candidate in top_candidates
        ]
    } 
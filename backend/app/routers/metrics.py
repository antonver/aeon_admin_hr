from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from datetime import datetime, timedelta

from backend.app.database import get_db, Candidate, InterviewLog
from backend.app.models import Metrics

router = APIRouter()

def get_date_range(period: str, scope: str):
    """Получить диапазон дат на основе периода и типа"""
    if scope == 'month':
        # period format: YYYY-MM
        year, month = map(int, period.split('-'))
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = datetime(year, month + 1, 1) - timedelta(days=1)
    else:  # scope == 'year'
        # period format: YYYY
        year = int(period)
        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31)
    
    return start_date, end_date

@router.get("/overview", response_model=Metrics)
async def get_metrics_overview(
    period: Optional[str] = Query(None, description="Период в формате YYYY-MM для месяца или YYYY для года"),
    scope: Optional[str] = Query(None, description="Тип периода: month или year"),
    db: Session = Depends(get_db)
):
    """Получить общие метрики с фильтрацией по периоду"""
    
    if period and scope:
        start_date, end_date = get_date_range(period, scope)
        
        # Общее количество кандидатов за период
        total_candidates = db.query(Candidate).filter(
            Candidate.created_at >= start_date,
            Candidate.created_at <= end_date
        ).count()
        
        # Прошедшие кандидаты за период
        passed_candidates = db.query(Candidate).filter(
            Candidate.status == "берем",
            Candidate.created_at >= start_date,
            Candidate.created_at <= end_date
        ).count()
        
        # Процент прохождения теста
        test_pass_rate = (passed_candidates / total_candidates * 100) if total_candidates > 0 else 0
    else:
        # Без фильтрации - все данные
        total_candidates = db.query(Candidate).count()
        passed_candidates = db.query(Candidate).filter(Candidate.status == "берем").count()
        test_pass_rate = (passed_candidates / total_candidates * 100) if total_candidates > 0 else 0
    
    return Metrics(
        total_candidates=total_candidates,
        passed_candidates=passed_candidates,
        test_pass_rate=round(test_pass_rate, 2),
    )

@router.get("/status-distribution")
async def get_status_distribution(
    period: Optional[str] = Query(None, description="Период в формате YYYY-MM для месяца или YYYY для года"),
    scope: Optional[str] = Query(None, description="Тип периода: month или year"),
    db: Session = Depends(get_db)
):
    """Получить распределение по статусам с фильтрацией по периоду"""
    
    if period and scope:
        start_date, end_date = get_date_range(period, scope)
        
        status_counts = db.query(
            Candidate.status,
            func.count(Candidate.id).label('count')
        ).filter(
            Candidate.created_at >= start_date,
            Candidate.created_at <= end_date
        ).group_by(
            Candidate.status
        ).all()
    else:
        # Без фильтрации - все данные
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
    period: Optional[str] = Query(None, description="Период в формате YYYY-MM для месяца или YYYY для года"),
    scope: Optional[str] = Query(None, description="Тип периода: month или year"),
    db: Session = Depends(get_db)
):
    """Получить активность по дням с фильтрацией по периоду"""
    
    if period and scope:
        start_date, end_date = get_date_range(period, scope)
        
        # Активность по дням за выбранный период
        activity = db.query(
            func.date(Candidate.last_action_date).label('date'),
            func.count(Candidate.id).label('count')
        ).filter(
            Candidate.last_action_date >= start_date,
            Candidate.last_action_date <= end_date
        ).group_by(
            func.date(Candidate.last_action_date)
        ).order_by(
            func.date(Candidate.last_action_date)
        ).all()
    else:
        # Без фильтрации - последние 30 дней
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30)
        
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
async def get_interview_stats(
    period: Optional[str] = Query(None, description="Период в формате YYYY-MM для месяца или YYYY для года"),
    scope: Optional[str] = Query(None, description="Тип периода: month или year"),
    db: Session = Depends(get_db)
):
    """Получить статистику интервью с фильтрацией по периоду"""
    
    if period and scope:
        start_date, end_date = get_date_range(period, scope)
        
        # Статистика интервью за период
        category_stats = db.query(
            InterviewLog.category,
            func.avg(InterviewLog.score).label('avg_score'),
            func.count(InterviewLog.id).label('count')
        ).join(
            Candidate, InterviewLog.candidate_id == Candidate.id
        ).filter(
            InterviewLog.score.isnot(None),
            InterviewLog.category.isnot(None),
            Candidate.created_at >= start_date,
            Candidate.created_at <= end_date
        ).group_by(
            InterviewLog.category
        ).all()
    else:
        # Без фильтрации - все данные
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
    period: Optional[str] = Query(None, description="Период в формате YYYY-MM для месяца или YYYY для года"),
    scope: Optional[str] = Query(None, description="Тип периода: month или year"),
    limit: int = Query(10, description="Количество кандидатов"),
    db: Session = Depends(get_db)
):
    """Получить топ кандидатов по среднему баллу с фильтрацией по периоду"""
    
    query = db.query(
        Candidate.full_name,
        func.avg(InterviewLog.score).label('avg_score'),
        func.count(InterviewLog.id).label('questions_count')
    ).join(
        InterviewLog, Candidate.id == InterviewLog.candidate_id
    ).filter(
        InterviewLog.score.isnot(None)
    )
    
    if period and scope:
        start_date, end_date = get_date_range(period, scope)
        query = query.filter(
            Candidate.created_at >= start_date,
            Candidate.created_at <= end_date
        )
    
    top_candidates = query.group_by(
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
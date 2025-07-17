from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from backend.db.db import get_db
from backend.db.models import Transaction, User
from backend.db.auth_utils import get_current_user

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)

@router.get("/summary")
def get_category_summary(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
  
    results = db.query(
        Transaction.category,
        func.sum(Transaction.amount).label("total_spent")
    ).filter(Transaction.user_id == current_user.id).group_by(Transaction.category).all()

    return [
        {"category": r[0], "total_spent": round(r[1], 2)}
        for r in results if r[0] is not None
    ]

@router.get("/suspicious-count")
def get_suspicious_count_by_bank(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Gets a count of suspicious transactions by bank for the current user.
    """
    results = db.query(
        Transaction.bank,
        func.count().label("suspicious_count")
    ).filter(
        Transaction.suspicious_reason.isnot(None),
        Transaction.user_id == current_user.id
    ).group_by(Transaction.bank).all()

    return [
        {"bank": r[0], "suspicious_count": r[1]}
        for r in results
    ]

@router.get("/daily")
def get_daily_spend(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
   
    today = datetime.now().date()
    last_week = today - timedelta(days=6)

    results = db.query(
        func.date(Transaction.timestamp).label("day"),
        func.sum(Transaction.amount).label("total_spent")
    ).filter(
        Transaction.user_id == current_user.id,
        func.date(Transaction.timestamp) >= last_week
    ).group_by(func.date(Transaction.timestamp)).order_by(func.date(Transaction.timestamp)).all()

    return [
        {"date": str(r[0]), "total_spent": round(r[1], 2)}
        for r in results
    ]

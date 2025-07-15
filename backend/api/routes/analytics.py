from fastapi import APIRouter
from sqlalchemy import func
from backend.db.db import SessionLocal
from backend.db.models import Transaction
from datetime import datetime, timedelta


router = APIRouter()

@router.get("/summary")
def get_category_summary():
    db = SessionLocal()
    results = db.query(
        Transaction.category,
        func.sum(Transaction.amount).label("total_spent")
    ).group_by(Transaction.category).all()
    db.close()

    return [
        {"category": r[0], "total_spent": round(r[1], 2)}
        for r in results
    ]

@router.get("/suspicious-count")
def get_suspicious_count_by_bank():
    db = SessionLocal()
    results = db.query(
        Transaction.bank,
        func.count().label("suspicious_count")
    ).filter(Transaction.suspicious_reason.isnot(None)) \
     .group_by(Transaction.bank).all()
    db.close()

    return [
        {"bank": r[0], "suspicious_count": r[1]}
        for r in results
    ]

@router.get("/daily")
def get_daily_spend():
    db = SessionLocal()

    # Get today and 6 days ago
    today = datetime.now().date()
    last_week = today - timedelta(days=6)

    # Group by DATE (not full timestamp)
    results = db.query(
        func.date(Transaction.timestamp).label("day"),
        func.sum(Transaction.amount).label("total_spent")
    ).filter(
        func.date(Transaction.timestamp) >= last_week
    ).group_by(func.date(Transaction.timestamp)) \
     .order_by(func.date(Transaction.timestamp)).all()

    db.close()

    return [
        {"date": str(r[0]), "total_spent": round(r[1], 2)}
        for r in results
    ]
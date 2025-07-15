from fastapi import APIRouter
from backend.db.db import SessionLocal
from backend.db.models import Transaction

router = APIRouter()

@router.get("/suspicious-transactions")
def get_suspicious_transactions():
    db = SessionLocal()
    txns = db.query(Transaction).filter(Transaction.suspicious_reason.isnot(None)).all()
    db.close()

    return [
        {
            "id": t.id,
            "bank": t.bank,
            "amount": t.amount,
            "description": t.description,
            "timestamp": t.timestamp,
            "account_number": t.account_number,
            "category": t.category,
            "suspicious_reason": t.suspicious_reason,
        }
        for t in txns
    ]

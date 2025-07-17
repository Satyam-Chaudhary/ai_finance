from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from backend.db.db import get_db
from backend.db.models import Transaction, User
from backend.db.auth_utils import get_current_user
from pydantic import BaseModel

router = APIRouter()

class TransactionResponse(BaseModel):
    id: str
    bank: str
    amount: float
    description: str
    timestamp: datetime
    category: str | None = None
    suspicious_reason: str | None = None

    class Config:
        orm_mode = True

@router.get("/all-transactions", response_model=List[TransactionResponse])
def get_all_transactions(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
 
    txns = db.query(Transaction).filter(Transaction.user_id == current_user.id).order_by(Transaction.timestamp.desc()).all()
    return txns

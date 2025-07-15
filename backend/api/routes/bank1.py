from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/transactions")
def get_transactions():
    return [
    {
        "id": "b1-tx1",
        "amt": 450.75,
        "desc": "Domino's Pizza",
        "ts": datetime.now().isoformat(),
        "acc": "XXXX1234"
    },
    {
        "id": "b1-tx2",
        "amt": 98000,
        "desc": "MacBook Pro - Apple Store",
        "ts": datetime.now().isoformat(),
        "acc": "XXXX1234"
    },
    {
        "id": "b1-tx3",
        "amt": 250000,
        "desc": "Gold bars from unknown merchant",
        "ts": datetime.now().isoformat(),
        "acc": "XXXX1234"
    },
    {
        "id": "b1-tx4",
        "amt": 500000,
        "desc": "Cash withdrawal from Dubai ATM",
        "ts": datetime.now().isoformat(),
        "acc": "XXXX1234"
    },
    {
        "id": "b1-tx5",
        "amt": 12999999,
        "desc": "Netflix Annual Subscription",
        "ts": datetime.now().isoformat(),
        "acc": "XXXX1234"
    },
    
]
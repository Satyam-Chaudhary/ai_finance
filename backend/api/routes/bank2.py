from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/transactions")
def get_transactions():
    return [
        {
            "transaction_id": "b2-tx1",
            "amount": "3200000000.00",
            "description": "Uber Ride to Airport",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "account_no": "XXXX5678"
        },
        {
            "transaction_id": "b2-tx2",
            "amount": "120000.00",
            "description": "Jewellery Purchase - Tanishq",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "account_no": "XXXX5678"
        },
        {
            "transaction_id": "b2-tx3",
            "amount": "5000.00",
            "description": "Grocery Shopping - Big Bazaar",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "account_no": "XXXX5678"
        },
        {
            "transaction_id": "b2-tx4",
            "amount": "25000.00",
            "description": "Electricity Bill Payment",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "account_no": "XXXX5678"
        }
    ]

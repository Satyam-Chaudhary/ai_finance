import time
import random
from datetime import datetime
from backend.db.models import Transaction
from backend.db.db import SessionLocal

MOCK_DESC = [
    "ATM Withdrawal - Delhi", "Zomato Order", "Flight to Dubai",
    "Luxury Watch Purchase", "Petrol Pump", "Amazon Kindle",
    "Large Electronics - Flipkart", "Transfer to Foreign Account",
    "Pizza", "Gold Coins Purchase"
]

CATEGORIES = ["food", "shopping", "travel", "others", "fuel", "rent", "transport"]

print("🚀 Stream script started...")
def simulate_transaction_stream():
    db = SessionLocal()
    while True:
        desc = random.choice(MOCK_DESC)
        amt = round(random.uniform(500, 200000), 2)
        cat = random.choice(CATEGORIES)

        txn = Transaction(
            id=f"stream-tx-{int(time.time())}",
            bank="stream-bank",
            amount=amt,
            description=desc,
            timestamp=datetime.now(),
            account_number="XXXXSTREAM",
            category=cat,
            suspicious_reason=None  # You can call LLM enrichment later
        )

        try:
            db.add(txn)
            db.commit()
            print(f"📥 [Streamed] {txn.description} ₹{txn.amount}")
        except Exception as e:
            print("❌ DB Error:", e)

        time.sleep(3)  

if __name__ == "__main__":
    simulate_transaction_stream()

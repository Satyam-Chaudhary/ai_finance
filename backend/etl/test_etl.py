import httpx
import json
from datetime import datetime

from backend.etl.etl import normalize_bank1, normalize_bank2
from backend.llm.llm_utils import enrich_transaction
from backend.db.db import init_db, SessionLocal
from backend.db.models import Transaction, User
from backend.db.auth_utils import hash_password
from backend.stream.kafka_producer import send_suspicious_to_kafka 
from backend.llm.llm_utils_2 import enrich_transaction2 

def get_or_create_default_user(db_session, default_email="test@example.com", password="testpassword"):
    
    # default_email = "test@example.com"
    user = db_session.query(User).filter_by(email=default_email).first()
    
    if not user:
        print(f"Default user not found. Creating user '{default_email}'...")
        user = User(
            email=default_email,
            hashed_password=hash_password("testpassword")
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        print(f"User '{default_email}' created with ID: {user.id}")
    
    return user

def test_etl_pipeline():
    db = SessionLocal()

    try:
        default_user = get_or_create_default_user(db)

        try:
            b1 = httpx.get("http://localhost:8001/bank1/transactions").json()
            # b2 = httpx.get("http://localhost:8001/bank2/transactions").json()
        except httpx.ConnectError:
            print("\n❌ Connection Error: Could not connect to the FastAPI server.")
            print("Please ensure the server is running in a separate terminal with 'uvicorn backend.api.main:app --port 8001'.")
            return

        bank1_clean = normalize_bank1(b1)
        # bank2_clean = normalize_bank2(b2)
        all_txns = bank1_clean
        

        print(f"\nProcessing transactions for user ID: {default_user.id}...")
        for tx in all_txns:
            # FIX: Add the user_id directly to the transaction dictionary
            tx['user_id'] = default_user.id
            unique_txn_id = f"user1-{tx['txn_id']}"
            
            enrich = enrich_transaction2(tx["description"], tx["amount"])
            tx.update(enrich)

            txn_obj = Transaction(
                id=unique_txn_id,
                bank=tx["bank"],
                amount=tx["amount"],
                description=tx["description"],
                timestamp=datetime.fromisoformat(tx["timestamp"]),
                account_number=tx["account_number"],
                category=tx["category"],
                suspicious_reason=tx["suspicious_reason"],
                user_id=tx["user_id"]
            )
            db.merge(txn_obj)

            if tx["suspicious_reason"]:
                tx['txn_id'] = unique_txn_id # this was leading to mismatch in data when queried from db and send to kafka in real time
                send_suspicious_to_kafka(tx)

        db.commit()
        print("\n✅ All transactions saved to SQLite DB.")

    except Exception as e:
        print(f"❌ An error occurred during the ETL process: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    init_db()
    db = SessionLocal()
    user = get_or_create_default_user(db)
    db.close()
    test_etl_pipeline()

if __name__ == "__main__":
    main()

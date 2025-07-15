import httpx
import json
from datetime import datetime

from backend.etl.etl import normalize_bank1, normalize_bank2
from backend.llm.llm_utils import enrich_transaction
from backend.db.db import init_db, SessionLocal
from backend.db.models import Transaction
from backend.stream.kafka_producer import send_suspicious_to_kafka  

def test_etl_pipeline():
    # 1. Init DB
    init_db()
    db = SessionLocal()

    # 2. Fetch mock bank data
    b1 = httpx.get("http://localhost:8001/bank1/transactions").json()
    b2 = httpx.get("http://localhost:8001/bank2/transactions").json()

    # 3. Normalize
    bank1_clean = normalize_bank1(b1)
    bank2_clean = normalize_bank2(b2)
    all_txns = bank1_clean + bank2_clean

    # 4. Enrich + Save + Send suspicious to Kafka
    for tx in all_txns:
        enrich = enrich_transaction(tx["description"], tx["amount"])
        tx.update(enrich)

        txn_obj = Transaction(
            id=tx["txn_id"],
            bank=tx["bank"],
            amount=tx["amount"],
            description=tx["description"],
            timestamp=datetime.fromisoformat(tx["timestamp"]),
            account_number=tx["account_number"],
            category=tx["category"],
            suspicious_reason=tx["suspicious_reason"]
        )

        db.merge(txn_obj) 

        # Send suspicious to Kafka
        if tx["suspicious_reason"]:
            print("⚠️ Suspicious:")
            print(json.dumps(tx, indent=2))
            send_suspicious_to_kafka(tx)  

    try:
        db.commit()
    except Exception as e:
        print("❌ DB Commit Failed:", e )
    db.close()

    print("\n✅ All transactions saved to SQLite DB.")

if __name__ == "__main__":
    test_etl_pipeline()

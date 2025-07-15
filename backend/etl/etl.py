from datetime import datetime


def normalize_bank1(txns):
    normalized = []
    for tx in txns:
        normalized.append({
            "txn_id": tx["id"],
            "bank": "bank1",
            "amount": float(tx["amt"]),
            "description": tx["desc"],
            "timestamp": tx["ts"],
            "account_number": tx["acc"]
        })
    return normalized


def normalize_bank2(txns):
    normalized = []
    for tx in txns:
        timestamp = f"{tx['date']}T00:00:00"
        normalized.append({
            "txn_id": tx["transaction_id"],
            "bank": "bank2",
            "amount": float(tx["amount"]),
            "description": tx["description"],
            "timestamp": timestamp,
            "account_number": tx["account_no"]
        })
    return normalized

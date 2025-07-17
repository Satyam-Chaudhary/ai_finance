from kafka import KafkaProducer
import json
from backend.config import SUSPICIOUS_TOPIC

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def send_suspicious_to_kafka(txn: dict):
    """
    Sends a transaction to Kafka.
    It's crucial that the 'user_id' is present in the txn dictionary.
    """
    if 'user_id' not in txn:
        print("❌ ERROR: 'user_id' missing from transaction. Cannot send to Kafka.")
        return
        
   
    user_id_bytes = str(txn['user_id']).encode('utf-8')
    producer.send(SUSPICIOUS_TOPIC, key=user_id_bytes, value=txn)
    producer.flush()
    print(f"Sent txn {txn['txn_id']} for user {txn['user_id']} to Kafka.")

from kafka import KafkaProducer
import json
from backend.config import SUSPICIOUS_TOPIC

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def send_suspicious_to_kafka(txn: dict):
    producer.send(SUSPICIOUS_TOPIC, txn)
    producer.flush()

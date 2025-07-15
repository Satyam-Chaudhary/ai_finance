import asyncio
import json
from kafka import KafkaConsumer
from backend.config import SUSPICIOUS_TOPIC


# Shared queue for WebSocket to consume from
suspicious_txn_queue = asyncio.Queue()

async def consume_suspicious_messages():
    consumer = KafkaConsumer(
        SUSPICIOUS_TOPIC,
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='suspicious-monitor-group',
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    )

    print("📡 Listening for suspicious transactions...\n")

    try:
        while True:
            raw_messages = consumer.poll(timeout_ms=1000)
            for tp, messages in raw_messages.items():
                for msg in messages:
                    txn = msg.value
                    print("⚠️ New Suspicious Transaction:")
                    print(json.dumps(txn, indent=2), "\n")

                    # Send to websocket broadcaster queue
                    await suspicious_txn_queue.put(txn)

            await asyncio.sleep(0.1)

    except asyncio.CancelledError:
        print("🛑 Kafka consumer shutting down...")
        consumer.close()

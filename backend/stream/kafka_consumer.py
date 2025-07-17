import asyncio
import json
from kafka import KafkaConsumer
from backend.config import SUSPICIOUS_TOPIC
from backend.api.ws import manager # Import the user-aware manager

async def consume_suspicious_messages():
    
    consumer = KafkaConsumer(
        SUSPICIOUS_TOPIC,
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='suspicious-user-notifier-group',
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    )

    print("📡 Listening for suspicious transactions to notify specific users...\n")

    try:
        while True:
            raw_messages = consumer.poll(timeout_ms=1000)
            if not raw_messages:
                await asyncio.sleep(0.1)
                continue

            for tp, messages in raw_messages.items():
                for msg in messages:
                    txn_data = msg.value
                    user_id = txn_data.get('user_id')

                    if user_id:
                        await manager.send_to_user(user_id, txn_data)
                    else:
                        print(f"⚠️ Message received without user_id: {txn_data.get('txn_id')}")
            
            await asyncio.sleep(0.1)

    except asyncio.CancelledError:
        print("🛑 Kafka consumer shutting down...")
    finally:
        consumer.close()

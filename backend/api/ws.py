from fastapi import APIRouter, WebSocket
from backend.stream.kafka_consumer import suspicious_txn_queue

router = APIRouter()

@router.websocket("/ws/suspicious")
async def websocket_suspicious_alerts(websocket: WebSocket):
    await websocket.accept()
    print("🧑‍💻 WebSocket client connected!")

    try:
        while True:
            txn = await suspicious_txn_queue.get()
            await websocket.send_json(txn)
    except Exception as e:
        print("❌ WebSocket closed:", e)

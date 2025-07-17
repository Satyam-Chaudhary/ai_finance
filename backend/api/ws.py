import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from typing import Dict, List

from backend.db.auth_utils import get_current_user
from backend.db.models import User
import asyncio

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
        print(f"✅ WebSocket connected for user {user_id}. Total connections for user: {len(self.active_connections[user_id])}")

    def disconnect(self, websocket: WebSocket, user_id: int):
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
        print(f"❌ WebSocket disconnected for user {user_id}.")

    async def send_to_user(self, user_id: int, message: dict):
        """Sends a message to all connections for a specific user."""
        if user_id in self.active_connections:
            message_str = json.dumps(message)
            # Create a list of tasks to send messages concurrently
            tasks = [conn.send_text(message_str) for conn in self.active_connections[user_id]]
            await asyncio.gather(*tasks)
            print(f"Sent message to user {user_id}.")

manager = ConnectionManager()

async def get_user_from_token(token: str):
    
    from backend.db import db
    from backend.db.auth_utils import decode_access_token
    
    payload = decode_access_token(token)
    if payload is None:
        return None
    user_id = payload.get("sub")
    if user_id is None:
        return None
    
    db_session = next(db.get_db())
    user = db_session.query(User).filter(User.id == int(user_id)).first()
    return user


@router.websocket("/ws/suspicious")
async def websocket_endpoint(websocket: WebSocket, token: str):
    
    user = await get_user_from_token(token)
    if user is None:
        await websocket.close(code=1008) # Policy Violation
        return

    await manager.connect(websocket, user.id)
    try:
        while True:
            # Keep the connection alive, listening for any messages from client (optional)
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, user.id)

# We need asyncio for gather


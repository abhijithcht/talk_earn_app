from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict
import json

router = APIRouter(prefix="/chat", tags=["chat"])

class ConnectionManager:
    def __init__(self):
        # Maps user_id -> WebSocket (Private 1-on-1 signaling)
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        self.active_connections.pop(user_id, None)

    async def send_personal_message(self, message: str, user_id: str):
        ws = self.active_connections.get(user_id)
        if ws:
            await ws.send_text(message)

manager = ConnectionManager()

class GlobalConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                pass # Connection might be closed

global_manager = GlobalConnectionManager()

@router.websocket("/ws/global/{user_name}")
async def global_websocket_endpoint(websocket: WebSocket, user_name: str):
    await global_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Broadcast incoming text as a JSON packet
            payload = json.dumps({
                "from_user": user_name,
                "message": data
            })
            await global_manager.broadcast(payload)
    except WebSocketDisconnect:
        global_manager.disconnect(websocket)
        await global_manager.broadcast(json.dumps({
            "from_user": "System",
            "message": f"{user_name} left the lobby"
        }))


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Expecting JSON: {"target_user_id": "...", "type": "offer/answer/candidate/text", "payload": "..."}
            try:
                msg = json.loads(data)
                target = msg.get("target_user_id")
                if target:
                    # Forward the WebRTC signaling or text message to the specific target user
                    await manager.send_personal_message(json.dumps({
                        "from_user_id": user_id,
                        "type": msg.get("type"),
                        "payload": msg.get("payload")
                    }), target)
            except json.JSONDecodeError:
                pass # invalid message format
    except WebSocketDisconnect:
        manager.disconnect(user_id)
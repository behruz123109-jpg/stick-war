from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import json
import database as db

app = FastAPI()

# Statik fayllarni (HTML, CSS, JS) ulash
app.mount("/static", StaticFiles(directory="static"), name="static")

# Xonalarni boshqarish
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict = {}

    async def connect(self, websocket: WebSocket, room_id: str):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)

    def disconnect(self, websocket: WebSocket, room_id: str):
        self.active_connections[room_id].remove(websocket)

    async def broadcast(self, message: str, room_id: str):
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                await connection.send_text(message)

manager = ConnectionManager()

@app.get("/")
async def serve_game():
    return FileResponse("static/index.html")

@app.get("/admin")
async def serve_admin():
    return FileResponse("static/admin.html")

# Reklama ko'rilganda olmos berish API
@app.post("/api/reward/{username}")
async def reward_player(username: str):
    reward_amount = db.get_setting('gem_reward')
    # Baza yangilanadi
    db.update_user_gems(username, reward_amount)
    return {"status": "success", "message": f"{reward_amount} olmos berildi!"}

# WebSocket Multiplayer Logic
@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await manager.connect(websocket, room_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Barcha o'yinchilarga harakatni jo'natish
            await manager.broadcast(data, room_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)

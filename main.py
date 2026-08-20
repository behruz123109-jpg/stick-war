from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import database as db
import asyncio

app = FastAPI()

# Vercel'dan kelayotgan ulanishlarga ruxsat berish (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Keyinchalik buni Vercel domeningga o'zgartirasan
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Server ishga tushganda Turso bazani tayyorlaymiz
@app.on_event("startup")
async def startup_event():
    await db.init_db()

# Render manzili ishlashini tekshirish uchun oddiy ping
@app.get("/")
async def root():
    return {"status": "Backend ishlamoqda. Vercel saytiga kiring."}

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict = {}

    async def connect(self, websocket: WebSocket, room_id: str):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)

    def disconnect(self, websocket: WebSocket, room_id: str):
        if room_id in self.active_connections:
            self.active_connections[room_id].remove(websocket)
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]

    async def broadcast(self, message: str, room_id: str):
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await manager.connect(websocket, room_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data, room_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)

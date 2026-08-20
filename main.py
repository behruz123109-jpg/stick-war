from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import json
import database as db

app = FastAPI()

# Frontend statik fayllarini ulash
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse("static/index.html")

# ---Qaysi loyiha uchun kod tayyorlab berishim kerak (masalan: Telegram bot, HTML/CSS veb-sayt yoki boshqa dastur)? 

Loyiha va uning vazifasini qisqacha aytsangiz, GitHub’ga to'g'ridan-to'g'ri yuklashga tayyor fayllar tuzilishi (`main.py`, `requirements.txt`, `.gitignore`, `README.md` va hokazo) bilan to'liq va tayyor kodni chiqarib beraman.

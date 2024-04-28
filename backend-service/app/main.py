from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from random import random
import time

app = FastAPI()

@app.get("/")
async def get():
    return "Welcome to starting page"

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        # data = await websocket.receive_text()
        await websocket.send_text(f"{round(random(), 2)}")

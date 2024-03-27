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
        await websocket.send_text(f"{random()}")

@app.websocket("/ws1")
async def websocket_endpoint1(websocket: WebSocket):
    await websocket.accept()
    while True:
        # data = await websocket.receive_text()
        await websocket.send_text(f"{random() + 100}")


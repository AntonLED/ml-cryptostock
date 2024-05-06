from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from random import random
import time
import app.services as services
import torch
import pandas as pd
import numpy as np
import joblib
import requests


app = FastAPI()

'''@app.get("/")
async def get_homepage():
    return "Welcome to starting page"'''

"""@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        # data = await websocket.receive_text()
        await websocket.send_text(f"{round(random(), 2)}")"""


def get_klines_iter():
    # TODO: fix this bullshit function
    url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m&limit=100"
    df = pd.DataFrame(pd.read_json(url)[1])
    df.columns = ["open"]

    return df


@app.get("/predict/")
async def get_predict():
    scaler = joblib.load("app/data/scaler.joblib")
    model = services.BTCModel()
    model.load_state_dict(
        torch.load("app/data/TransformerBTC.pt", map_location=torch.device("cpu"))
    )
    model.eval()

    df = get_klines_iter()
    real_value = df["open"].values[-1]
    df.reset_index(drop=True, inplace=True)
    data = scaler.transform(df)

    for _ in range(100):
        tensor = services.create_dataset(data)
        pred = services.predict(model, tensor)
        data = np.append(data, np.array(pred))
        data = data[1:]

    preds = pd.DataFrame(data)
    unscaled = scaler.inverse_transform(preds)
    predicted_value = unscaled.flatten().tolist()[0]

    return {"real_value": real_value, "predicted_value": predicted_value}

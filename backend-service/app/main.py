from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import app.services as services
import numpy as np


app = FastAPI()

@app.get("/")
async def get_homepage():
    return "Welcome to starting page"

@app.on_event("startup")
async def startup_event():
    services.GetHistoricalData()

@app.get("/predict/")
async def get_predict():
    pred = services.GetPrediction()
    return {"preds" : np.reshape(pred, (100)).tolist()}



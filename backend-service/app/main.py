from fastapi import FastAPI
import app.services as services

app = FastAPI()

@app.get("/")
async def get_homepage():
    return "Welcome to starting page"

@app.on_event("startup")
async def startup_event():
    services.GetHistoricalData()

@app.get("/predict/")
async def get_predict():
    return services.GetPrediction()



from typing import List
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import app.services as services
import torch
import pandas as pd
import numpy as np
import joblib
import datetime
import random

from app.db import crud, models, schemas
from app.db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


def get_klines_iter(symbol: str, interval: str, limit: int):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    df = pd.DataFrame(pd.read_json(url)[1])
    # df.columns = ["open"]

    return df["open"]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/clear_rvs/")
def clear_rvs(db: Session = Depends(get_db)):
    return crud.clear_real_values(db)


@app.get("/clear_pvs/")
def clear_pvs(db: Session = Depends(get_db)):
    return crud.clear_predicted_values(db)


@app.post("/set_rv/", response_model=schemas.RealValue)
def app_rv(rv: schemas.RealValueCreate, db: Session = Depends(get_db)):
    return crud.add_real_value(db, real_value=rv)


@app.post("/set_pv/", response_model=schemas.PredictedValue)
def add_pv(pv: schemas.PredictedValueCreate, db: Session = Depends(get_db)):
    return crud.add_predicted_value(db, predicted_value=pv)


@app.get("/get_rvs/", response_model=List[schemas.RealValue])
def read_rvs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rvs = crud.get_real_values(db, skip=skip, limit=limit)
    return rvs


@app.get("/get_pvs/", response_model=List[schemas.PredictedValue])
def read_pvs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pvs = crud.get_predicted_values(db, skip=skip, limit=limit)
    return pvs


@app.get("/predict/")
async def get_predict():
    return {"time": datetime.datetime.now(), "value": round(random.random(), 2)}


# @app.post("/upd_rvs/")
# def update_rvs(
#     symbol: str = "BTCUSDT",
#     interval: str = "1m",
#     limit: int = 100,
#     db: Session = Depends(get_db),
# ):
#     rvs = get_klines_iter(symbol, interval, limit)
#     for rv in rvs:
#         crud.add_real_value(
#             db, real_value=schemas.RealValueCreate(value=rv, currency=symbol)
#         )


# @app.get("/predict/")
# async def get_predict():
#     scaler = joblib.load("app/data/scaler.joblib")
#     model = services.BTCModel()
#     model.load_state_dict(
#         torch.load("app/data/TransformerBTC.pt", map_location=torch.device("cpu"))
#     )
#     model.eval()

#     df = get_klines_iter()
#     real_value = df["open"].values[-1]
#     df.reset_index(drop=True, inplace=True)
#     data = scaler.transform(df)

#     for _ in range(100):
#         tensor = services.create_dataset(data)
#         pred = services.predict(model, tensor)
#         data = np.append(data, np.array(pred))
#         data = data[1:]

#     preds = pd.DataFrame(data)
#     unscaled = scaler.inverse_transform(preds)
#     predicted_value = unscaled.flatten().tolist()[0]

#     return {"real_value": real_value, "predicted_value": predicted_value}

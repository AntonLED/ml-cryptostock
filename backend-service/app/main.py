from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import app.services as services
import torch
import pandas as pd
import numpy as np
import joblib

from app.db import crud, models, schemas
from app.db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/rv/", response_model=schemas.RealValue)
def app_rv(rv: schemas.RealValue, db: Session = Depends(get_db)):
    return crud.add_real_value(db, real_value=rv)


@app.post("/pv/", response_model=schemas.PredictedValue)
def add_pv(pv: schemas.PredictedValue, db: Session = Depends(get_db)):
    return crud.add_predicted_value(db, predicted_value=pv)


@app.get("/rvs/", response_model=List[schemas.RealValue])
def read_rvs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rvs = crud.get_real_values(db, skip=skip, limit=limit)
    return rvs


@app.get("/pvs/", response_model=List[schemas.PredictedValue])
def read_pvs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pvs = crud.get_predicted_values(db, skip=skip, limit=limit)
    return pvs


# def get_klines_iter():
#     # TODO: fix this bullshit function
#     url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m&limit=100"
#     df = pd.DataFrame(pd.read_json(url)[1])
#     df.columns = ["open"]

#     return df


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

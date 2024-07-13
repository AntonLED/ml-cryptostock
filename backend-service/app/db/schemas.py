from typing import Union

from pydantic import BaseModel


class RealValue(BaseModel):
    id: int
    value: float
    currency: str

    class Config:
        orm_mode = True


class PredictedValue(BaseModel):
    id: int
    value: float
    currency: str

    class Config:
        orm_mode = True

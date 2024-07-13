from typing import Union

from pydantic import BaseModel


class RealValueCreate(BaseModel):
    value: float
    currency: str


class RealValue(RealValueCreate):
    id: int

    class Config:
        from_attributes = True


class PredictedValueCreate(BaseModel):
    value: float
    currency: str


class PredictedValue(PredictedValueCreate):
    id: int

    class Config:
        from_attributes = True

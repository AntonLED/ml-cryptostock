from sqlalchemy import Column, Integer, String, Float

from app.db.database import Base


class RealValue(Base):
    __tablename__ = "real-values"

    id = Column(Integer, primary_key=True)
    value = Column(Float, index=True)
    currency = Column(String, index=True)


class PredictedValue(Base):
    __tablename__ = "predicted-values"

    id = Column(Integer, primary_key=True)
    value = Column(Float, index=True)
    currency = Column(String, index=True)

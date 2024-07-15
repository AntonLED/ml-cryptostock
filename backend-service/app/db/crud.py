from sqlalchemy.orm import Session

from app.db import models, schemas


def get_real_value(db: Session, id: int):
    return db.query(models.RealValue).filter(models.RealValue.id == id).first()


def get_real_values(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.RealValue).offset(skip).limit(limit).all()


def get_predicted_value(db: Session, id: int):
    return (
        db.query(models.PredictedValue).filter(models.PredictedValue.id == id).first()
    )


def get_predicted_values(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.PredictedValue).offset(skip).limit(limit).all()


def add_real_value(db: Session, real_value: schemas.RealValueCreate):
    db_rv = models.RealValue(value=real_value.value, currency=real_value.currency)
    db.add(db_rv)
    db.commit()
    db.refresh(db_rv)
    return db_rv


def add_predicted_value(db: Session, predicted_value: schemas.PredictedValueCreate):
    db_pv = models.PredictedValue(
        value=predicted_value.value, currency=predicted_value.currency
    )
    db.add(db_pv)
    db.commit()
    db.refresh(db_pv)
    return db_pv


def clear_predicted_values(db: Session):
    db.query(models.PredictedValue).delete()
    db.commit()
    return True


def clear_real_values(db: Session):
    db.query(models.RealValue).delete()
    db.commit()
    return True

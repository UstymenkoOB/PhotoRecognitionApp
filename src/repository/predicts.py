from sqlalchemy.orm import Session
from src.database.models import Prediction
from schemas import PredictionCreate
from datetime import datetime

def create_prediction(db: Session, prediction: PredictionCreate):
    db_prediction = Prediction(
        prediction_date=prediction.prediction_date,
        filename=prediction.filename,
        url=prediction.url,
        predicted_label=prediction.predicted_label
    )
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    return db_prediction

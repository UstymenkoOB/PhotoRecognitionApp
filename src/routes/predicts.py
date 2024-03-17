from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.repository.predicts import create_prediction
from src.schemas import PredictionCreate
from datetime import datetime

router = APIRouter(prefix='/predicts', tags=["prediction"])

def db_dependency():
    db = get_db()
    try:
        yield db
    finally:
        db.close()

@router.post("/predict/image")
async def predict_image(prediction: PredictionCreate, db: Session = Depends(db_dependency)):
    prediction.prediction_date = datetime.now()
    return create_prediction(db=db, prediction=prediction)

@router.post("/predict/url")
async def predict_image_url(prediction: PredictionCreate, db: Session = Depends(db_dependency)):
    prediction.prediction_date = datetime.now()
    return create_prediction(db=db, prediction=prediction)

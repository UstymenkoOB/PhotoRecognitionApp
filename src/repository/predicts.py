from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database.models import Prediction


async def create_prediction(filename: str, url: str, predicted_label: str, db: AsyncSession) -> Prediction:
    """
    Creates a prediction entry in the database.

    :param db: AsyncSession: A connection to the Postgres SQL database.
    :param prediction: PredictionCreate: The prediction data to be stored.
    :return: Prediction: The created prediction object.
    """
    prediction_date = datetime.now()
    db_prediction = Prediction(
        prediction_date=prediction_date,
        filename=filename,
        url=url,
        predicted_label=predicted_label
    )
    
    try:
        db.add(db_prediction)
        await db.commit()
        await db.refresh(db_prediction)
        return db_prediction
    except Exception as e:
        return None


async def get_predictions(limit: int, offset: int, db: AsyncSession):
    """
    Retrieves a list of predictions from the database.

    :param limit: int: The number of predictions to return.
    :param offset: int: The number of predictions to skip.
    :param db: AsyncSession: A connection to the Postgres SQL database.
    :return: list: A list of prediction objects.
    """

    result = await db.execute(select(Prediction).order_by(Prediction.prediction_date.desc()).limit(limit).offset(offset))
    predicts = result.fetchall()
    if predicts:
        pr_dick = []
        for o in predicts:
            pr_dick.append(o[0])
        return pr_dick
    else:
        return None

from fastapi import APIRouter, UploadFile, File, Request, Depends, Form, requests, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from io import BytesIO
from keras.models import load_model
from PIL import Image
from urllib.parse import urlparse
import numpy as np
import requests
import base64
import imghdr

from src.database.db import get_db
from src.repository.predicts import create_prediction
from src.repository.predicts import get_predictions as fetch_predictions
from src.schemas import PredictionCreate, PredictionModel

router = APIRouter(prefix='/predicts', tags=["predicts"])
model = load_model('Models/cifar10_best_latest.h5')

templates = Jinja2Templates(directory="templates")
class_labels = ['Літак', 'Автомобіль', 'Птах', 'Кіт',
                'Олень', 'Собака', 'Жаба', 'Кінь', 'Корабель', 'Вантажівка']



@router.post("/image", response_class=HTMLResponse, name="api_predict_image")
async def predict_image(request: Request, 
                        file: UploadFile = File(None),
                        db: AsyncSession = Depends(get_db)):
    if file is None:
        return templates.TemplateResponse("recognition.html", {"request": request,
                                                               "error": "Please, upload a file"})

    file_type = imghdr.what(None, h=file.file.read(2048))

    if not file_type:
        return templates.TemplateResponse("recognition.html", {"request": request,
                                                               "error": "Please, upload a file"})

    file.file.seek(0)
    f = file.file.read()
    image = Image.open(file.file)
    image = image.resize((32, 32)).convert('RGB')
    image_array = np.array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)

    prediction = model.predict(image_array)
    predicted_class = np.argmax(prediction)
    predicted_label = class_labels[predicted_class]
    image_base64 = base64.b64encode(f).decode('utf-8')
    print(file.filename)

    
    await create_prediction(filename=file.filename, url='', predicted_label=predicted_label, db=db)
    
    return templates.TemplateResponse("recognition.html", {"request": request,
                                                           "predicted_label": predicted_label,
                                                           "image_base64": image_base64})


@router.post("/url", response_class=HTMLResponse, name="api_predict_url")
async def predict_image_url(request: Request, 
                            url: str = Form(None),
                            db: AsyncSession = Depends(get_db)):
    if not url:
        return templates.TemplateResponse("recognition.html", {"request": request,
                                                               "error": "Please provide a URL"})

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return templates.TemplateResponse("recognition.html", {"request": request,
                                                               "error": f"Error downloading image from URL: {e}"})
    f = response.content
    image = Image.open(BytesIO(f))
    image = image.resize((32, 32)).convert('RGB')
    image_array = np.array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)

    prediction = model.predict(image_array)
    predicted_class = np.argmax(prediction)
    predicted_label = class_labels[predicted_class]
    image_base64 = base64.b64encode(f).decode('utf-8')

    filename = urlparse(url).path.split("/")[-1]
    
    await create_prediction(filename=filename, url=url, predicted_label=predicted_label, db=db)

    return templates.TemplateResponse("recognition.html", {"request": request,
                                                           "predicted_label": predicted_label,
                                                           "image_base64": image_base64})


@router.get("/", response_model=list[PredictionModel])
async def get_predictions(limit: int = Query(10, le=50), offset: int = 0, db: AsyncSession = Depends(get_db)):
    """
    Retrieves a list of predictions from the database.

    :param limit: int: The number of predictions to return.
    :param offset: int: The number of predictions to skip.
    :param db: AsyncSession: A connection to the Postgres SQL database.
    :return: list: A list of prediction objects.
    """
    predictions = await fetch_predictions(limit, offset, db)
    return predictions

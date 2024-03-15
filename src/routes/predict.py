from fastapi import APIRouter, UploadFile, File, Request, Form, requests
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from io import BytesIO
from keras.models import load_model
from PIL import Image
import numpy as np
import requests
import base64
import imghdr

router = APIRouter(prefix='/api', tags=["predict"])
model = load_model('Models/cifar10_best1.h5')
templates = Jinja2Templates(directory="templates")


@router.post("/predict/image", response_class=HTMLResponse, name="api_predict_image")
async def predict_image(request: Request, file: UploadFile = File(None)):
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

    class_labels = ['Літак', 'Автомобіль', 'Птах', 'Кіт',
                    'Олень', 'Собака', 'Жаба', 'Кінь', 'Корабель', 'Вантажівка']

    prediction = model.predict(image_array)
    predicted_class = np.argmax(prediction)
    predicted_label = class_labels[predicted_class]
    image_base64 = base64.b64encode(f).decode('utf-8')

    return templates.TemplateResponse("recognition.html", {"request": request,
                                                           "predicted_label": predicted_label,
                                                           "image_base64": image_base64})


@router.post("/predict/url", response_class=HTMLResponse, name="api_predict_url")
async def predict_image_url(request: Request, url: str = Form(None)):
    if not url:
        print("Not file")
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

    class_labels = ['Літак', 'Автомобіль', 'Птах', 'Кіт',
                    'Олень', 'Собака', 'Жаба', 'Кінь', 'Корабель', 'Вантажівка']

    prediction = model.predict(image_array)
    predicted_class = np.argmax(prediction)
    predicted_label = class_labels[predicted_class]
    image_base64 = base64.b64encode(f).decode('utf-8')

    return templates.TemplateResponse("recognition.html", {"request": request,
                                                           "predicted_label": predicted_label,
                                                           "image_base64": image_base64})

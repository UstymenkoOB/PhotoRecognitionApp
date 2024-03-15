from fastapi import APIRouter, UploadFile, File, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from keras.models import load_model
from PIL import Image
import numpy as np
import io
import base64

router = APIRouter(prefix='/api', tags=["predict"])
model = load_model('Models/cifar10_best1.h5')
templates = Jinja2Templates(directory="templates")

@router.post("/predict/", response_class=HTMLResponse, name="api_predict")
async def predict_image(request: Request, file: UploadFile = File(...)):
    f = file.file.read()
    image = Image.open(io.BytesIO(f))
    image = image.resize((32, 32))
    image_array = np.array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)

    class_labels = ['Літак', 'Автомобіль', 'Птах', 'Кіт',
                    'Олень', 'Собака', 'Жаба', 'Кінь', 'Корабель', 'Вантажівка']

    prediction = model.predict(image_array)
    predicted_class = np.argmax(prediction)
    predicted_label = class_labels[predicted_class]
    image_base64 = base64.b64encode(f).decode('utf-8')

    return templates.TemplateResponse("recognition.html", {"request": request, "predicted_label": predicted_label, "image_base64": image_base64})
 

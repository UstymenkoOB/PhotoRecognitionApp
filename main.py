from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from src.routes import predict
# from src.routes import user_profile
# from src.routes import auth
# from src.routes import picteres
# from src.routes import roles
# from src.routes import comments
# from src.routes import healthchecker

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", name='Home', response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": "Photo App"})


@app.get("/recognition", name='Recognition', response_class=HTMLResponse)
async def recognition(request: Request):
    return templates.TemplateResponse("recognition.html", {"request": request, "message": "Image Recognition Page"})


@app.get("/team", name='Team', response_class=HTMLResponse)
async def about_us(request: Request):
    return templates.TemplateResponse("about_us.html", {"request": request, "message": "About Us Page"})

app.include_router(predict.router, prefix='/api')
# app.include_router(healthchecker.router, prefix="/api")
# app.include_router(auth.router, prefix="/api")
# app.include_router(user_profile.profile_router, prefix="/api")
# app.include_router(roles.router, prefix='/api')
# app.include_router(picteres.router, prefix='/api')
# app.include_router(comments.router, prefix='/api')

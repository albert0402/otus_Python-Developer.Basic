from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

import os

# Entry point to app with FastAPI usage
app = FastAPI()

# Give the information about the templates dir
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(f'Working directory is: {os.getcwd()}')
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Give the information about the pictures dir
app.mount("/pictures", StaticFiles(directory="pictures"), name="pictures")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Главная страница"})

@app.get("/contacts/", response_class=HTMLResponse)
async def contacts(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request, "title": "Контакты"})

@app.get("/delivery/", response_class=HTMLResponse)
async def delivery(request: Request):
    return templates.TemplateResponse("delivery.html", {"request": request, "title": "Доставка"})

@app.get("/map/", response_class=HTMLResponse)
async def map(request: Request):
    return templates.TemplateResponse("map.html", {"request": request, "title": "Как добраться"})

@app.get("/about/", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request, "title": "О нас"})


if __name__ == '__main__':
    uvicorn.run("app:app", host='127.0.0.1', port=8000)
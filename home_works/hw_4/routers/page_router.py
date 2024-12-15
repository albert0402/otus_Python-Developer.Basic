from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import os

# Initialize the router for page
page_router = APIRouter()

# Configure the templates directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "../templates"))

# Route for the home page
@page_router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Главная страница"})

# Route for the "Contacts" page
@page_router.get("/contacts/", response_class=HTMLResponse)
async def contacts(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request, "title": "Контакты"})

# Route for the "Delivery" page
@page_router.get("/delivery/", response_class=HTMLResponse)
async def delivery(request: Request):
    return templates.TemplateResponse("delivery.html", {"request": request, "title": "Доставка"})

# Route for the "How to Get There" page
@page_router.get("/map/", response_class=HTMLResponse)
async def map(request: Request):
    return templates.TemplateResponse("map.html", {"request": request, "title": "Как добраться"})

# Route for the "About Us" page
@page_router.get("/about/", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request, "title": "О нас"})
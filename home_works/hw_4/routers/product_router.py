from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import os

# Инициализация роутера для продуктов
product_router = APIRouter()

# Конфигурация Jinja для шаблонов
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Конфигурируем директорию шаблонов
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "../templates"))

EXCEL_FILE_PATH = os.path.join(BASE_DIR, "../products.xlsx")

# Функция для загрузки данных из Excel по категории
def load_products_from_excel(category: str = None):
    try:
        # Загружаем Excel файл
        df = pd.read_excel(EXCEL_FILE_PATH, sheet_name=0)
        
        # Фильтруем по категории, если она указана
        if category:
            df = df[df["category"] == category]
        
        # Преобразуем в список словарей
        products = df.to_dict(orient="records")
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading data from Excel: {str(e)}")


# Общая функция для отображения страницы продуктов по категории
@product_router.get("/{category}", response_class=HTMLResponse)
async def get_category_page(request: Request, category: str, name: str = None):
    try:
        # Загружаем продукты для указанной категории
        products = load_products_from_excel(category)
        
        # Если имя указано, фильтруем продукты по имени
        if name:
            products = [product for product in products if name.lower() in product["name"].lower()]
        
        # Возвращаем страницу с продуктами для данной категории
        return templates.TemplateResponse(f"{category}.html", {"request": request, "products": products, "title": category.capitalize()})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

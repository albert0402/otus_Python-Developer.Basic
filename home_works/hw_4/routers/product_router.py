from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import os

# Initialize router for products
product_router = APIRouter()

# Jinja configuration for templates
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Configuring the templates directory
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "../templates"))

EXCEL_FILE_PATH = os.path.join(BASE_DIR, "../products.xlsx")

# Function to load product data from Excel by category
def load_products_from_excel(category: str = None):
    try:
        # Load the Excel file
        df = pd.read_excel(EXCEL_FILE_PATH, sheet_name=0)
        
        # Filter by category if specified
        if category:
            df = df[df["category"] == category]
        
        # Convert to a list of dictionaries
        products = df.to_dict(orient="records")
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading data from Excel: {str(e)}")


# General function to display product page by category
@product_router.get("/{category}", response_class=HTMLResponse)
async def get_category_page(request: Request, category: str, name: str = None):
    try:
        # Load products for the specified category
        products = load_products_from_excel(category)
        
        # If name is specified, filter products by name
        if name:
            products = [product for product in products if name.lower() in product["name"].lower()]
        
        # Return page with products for the given category
        return templates.TemplateResponse(f"{category}.html", {"request": request, "products": products, "title": category.capitalize()})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

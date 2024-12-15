from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import uvicorn
import os
import pandas as pd

from routers.page_router import page_router
from routers.product_router import product_router

# Create a FastAPI application
app = FastAPI()

# Configure the static directory for images
app.mount("/pictures", StaticFiles(directory="pictures"), name="pictures")

# Include the page routers for pages
app.include_router(page_router)
app.include_router(product_router, prefix="/api/products", tags=["products"])

# Entry point to run the application
if __name__ == '__main__':
    uvicorn.run("app:app", host='127.0.0.1', port=8000)
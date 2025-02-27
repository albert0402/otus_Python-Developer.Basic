from fastapi import FastAPI
from app.routers import users, posts
from app.services.data_loader import main as load_data

app = FastAPI(title="FastAPI Project")

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])


@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Application!"}


@app.on_event("startup")
async def startup_event():
    await load_data()

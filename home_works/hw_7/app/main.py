from fastapi import FastAPI
from app.routers import users, posts

app = FastAPI(title="FastAPI Project")

# Подключение роутеров
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Application!"}
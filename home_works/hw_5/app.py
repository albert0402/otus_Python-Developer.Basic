import uvicorn
from fastapi import FastAPI

# Create a FastAPI application
app = FastAPI()

@app.get("/ping/")
async def ping():
    return {"message": "pong"}

# Entry point to run the application
if __name__ == '__main__':
    uvicorn.run("app:app", host='0.0.0.0', port=8000)
from fastapi import FastAPI
from .config import Config

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
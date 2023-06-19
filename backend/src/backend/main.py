from fastapi import FastAPI
from backend.endpoints import healtcheck

app = FastAPI()

app.include_router(healtcheck.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}

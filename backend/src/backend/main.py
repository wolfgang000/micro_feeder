from fastapi import FastAPI
from backend.endpoints import healtcheck
from backend.endpoints.web import subscription

app = FastAPI()

app.include_router(healtcheck.router)
app.include_router(subscription.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}

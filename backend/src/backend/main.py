from fastapi import FastAPI
from backend.config import Config
from backend.endpoints import healtcheck
from backend.endpoints.web import subscription, auth
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=Config.SECRET_KEY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[Config.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(healtcheck.router)
app.include_router(subscription.router)
app.include_router(auth.router)

if Config.ENV in ["dev", "test"]:
    from backend.endpoints import testing

    app.include_router(testing.router)

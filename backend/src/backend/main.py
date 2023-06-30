from fastapi import FastAPI
from backend.config import Config
from backend.endpoints import healtcheck
from backend.endpoints.web import subscription, auth
from starlette.middleware.sessions import SessionMiddleware


app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=Config.SECRET_KEY)
app.include_router(healtcheck.router)
app.include_router(subscription.router)
app.include_router(auth.router)

if Config.ENV in ["dev", "test"]:
    from backend.endpoints import testing

    app.include_router(testing.router)

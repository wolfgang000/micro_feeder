from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from backend.config import Config
from backend.endpoints import healtcheck
from backend.endpoints.web import subscription, auth
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=Config.SECRET_KEY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[Config.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors: dict = {}
    for error in exc.errors():
        (_, field_name) = error["loc"]
        msg = error["msg"]
        error_field = errors.get(field_name, [])
        error_field.append(msg)
        errors[field_name] = error_field

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": errors}),
    )


app.include_router(healtcheck.router)
app.include_router(subscription.router)
app.include_router(auth.router)

if Config.ENV in ["dev", "test"]:
    from backend.endpoints import testing

    app.include_router(testing.router)

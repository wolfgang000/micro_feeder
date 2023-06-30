from __future__ import annotations
import os


def get_env_or_raise_exception(env_var_name: str) -> str:
    env_var = os.getenv(env_var_name)
    if env_var:
        return env_var
    raise Exception(f"Environment variable '{env_var_name}' could not be found")


ENV = get_env_or_raise_exception("ENV")

if ENV not in ["dev", "test", "prod"]:
    raise Exception(f"Wrong 'ENV'")

DATABASE_URL = get_env_or_raise_exception("DATABASE_URL")

if ENV == "test":
    DATABASE_URL = f"{DATABASE_URL}_test"


class Config:
    DATABASE_URL = DATABASE_URL
    DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "10"))
    RABBITMQ_URL = get_env_or_raise_exception("RABBITMQ_URL")
    REDIS_URL = get_env_or_raise_exception("REDIS_URL")
    GOOGLE_CLIENT_ID = get_env_or_raise_exception("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = get_env_or_raise_exception("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI = get_env_or_raise_exception("GOOGLE_REDIRECT_URI")
    FRONTEND_URL = get_env_or_raise_exception("FRONTEND_URL")
    SECRET_KEY = get_env_or_raise_exception("SECRET_KEY")
    ENV = ENV

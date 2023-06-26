from __future__ import annotations
import os

database_url_env_name = "DATABASE_URL"

if os.environ.get("ENV_TEST"):
    database_url_env_name = "TEST_DATABASE_URL"


def get_env_or_raise_exception(env_var_name: str) -> str:
    env_var = os.getenv(env_var_name)
    if env_var:
        return env_var
    raise Exception(f"Environment variable '{env_var_name}' could not be found")


class Config:
    DATABASE_URL = get_env_or_raise_exception(database_url_env_name)
    RABBITMQ_URL = get_env_or_raise_exception("RABBITMQ_URL")
    REDIS_URL = get_env_or_raise_exception("REDIS_URL")
    DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "10"))
    GOOGLE_CLIENT_ID = get_env_or_raise_exception("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = get_env_or_raise_exception("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI = get_env_or_raise_exception("GOOGLE_REDIRECT_URI")

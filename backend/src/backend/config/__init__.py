from __future__ import annotations
import os

def get_env_or_raise_exception(env_var_name: str) -> str:
    env_var = os.getenv(env_var_name)
    if env_var:
        return env_var
    raise Exception(f"Environment variable '{env_var_name}' could not be found")

class Config:
    DATABASE_URL = get_env_or_raise_exception("DATABASE_URL")
    DB_POOL_SIZE = int(get_env_or_raise_exception("DB_POOL_SIZE"))


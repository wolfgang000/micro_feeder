from typing import Generator
from fastapi.testclient import TestClient
import pytest
from . import db_helper
import alembic.config
from backend.main import app
from uuid import uuid4


@pytest.fixture(scope="session")
def clear_db():
    with db_helper.sql_connect_test() as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute("DROP SCHEMA public CASCADE;")
            cursor.execute("CREATE SCHEMA public;")
    alembicArgs = [
        "--raiseerr",
        "upgrade",
        "head",
    ]
    alembic.config.main(argv=alembicArgs)


def setup_db():
    with db_helper.sql_connect() as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            try:
                cursor.execute("DROP DATABASE %s  ;" % "postgres_dev_test")
            except Exception as e:
                pass
            cursor.execute("CREATE DATABASE %s  ;" % "postgres_dev_test")
    alembicArgs = [
        "--raiseerr",
        "upgrade",
        "head",
    ]
    alembic.config.main(argv=alembicArgs)


@pytest.hookimpl()
def pytest_sessionstart(session):
    setup_db()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def authenticated_client(client: TestClient) -> Generator:
    email = f"{uuid4()}@example.com"
    response = client.get(
        "/testing/create_user_and_login/",
        params={"user_email": email},
        follow_redirects=False,
    )
    assert response.status_code == 307
    yield client
import pytest
from . import db_helper
import alembic.config


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

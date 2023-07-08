from backend.core.services import create_user
from backend.core import models, unit_of_work
from fastapi.testclient import TestClient
from backend.main import app
from starlette.responses import JSONResponse
from uuid import uuid4


def create_authenticated_client():
    email = f"{uuid4()}@example.com"
    client = TestClient(app)
    response = client.get(
        "/testing/create_user_and_login/",
        params={"user_email": email},
        follow_redirects=False,
    )
    assert response.status_code == 307
    return client

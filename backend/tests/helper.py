from backend.core.services import create_user
from backend.core import models, unit_of_work
from fastapi.testclient import TestClient
from backend.main import app
from starlette.responses import JSONResponse
from uuid import uuid4


async def create_user_and_login(request):
    data = await request.json()
    email = data["email"]
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    user = await create_user(uow, {"email": email})
    request.session.update({"user_id": user.id})
    return JSONResponse({"user_id": user.id})


app.add_route("/create_user_and_login", create_user_and_login, methods=["POST"])


def create_authenticated_client():
    email = f"{uuid4()}@example.com"
    client = TestClient(app)
    response = client.post("/create_user_and_login", json={"email": email})
    assert response.status_code == 200
    return client

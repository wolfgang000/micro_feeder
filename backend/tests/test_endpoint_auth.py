from fastapi.testclient import TestClient
from backend.main import app
from result import Ok
from starlette.responses import JSONResponse
from starlette.routing import Route


async def view_session(request):
    return JSONResponse({"session": request.session})


async def update_session(request):
    data = await request.json()
    request.session.update(data)
    return JSONResponse({"session": request.session})


async def clear_session(request):
    request.session.clear()
    return JSONResponse({"session": request.session})


app.add_route("/view_session", view_session, methods=["GET"])
app.add_route("/update_session", update_session, methods=["POST"])
app.add_route("/clear_session", clear_session, methods=["POST"])


def test_login_redirect_to_google_login():
    client = TestClient(app)
    response = client.get("/web/auth/login", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"].startswith("https://accounts.google.com")


def test_login_redirect_to_dashboard_when_already_logged_in():
    client = TestClient(app)
    response = client.post("/update_session", json={"user_id": 123})
    assert response.status_code == 200

    response = client.get("/web/auth/login", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"].endswith("/dashboard")


def test_successful_login_callback(mocker):
    client = TestClient(app)

    mocker.patch(
        "backend.endpoints.web.auth.client.fetch_token",
        return_value=Ok({"access_token": "123"}),
    )

    mocker.patch(
        "backend.endpoints.web.auth.get_account_info",
        return_value=Ok({"email": "test@example.com"}),
    )

    response = client.get(
        "/web/auth/callback", params={"code": "123"}, follow_redirects=False
    )
    assert response.status_code == 307
    assert response.headers["location"].endswith("/dashboard")

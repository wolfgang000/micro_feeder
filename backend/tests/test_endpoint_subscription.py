import json
import os
import pytest
from fastapi.testclient import TestClient
from backend.main import app
from .helper import create_authenticated_client

FAKE_SERVER_URL = os.getenv("FAKE_SERVER_URL")

@pytest.mark.usefixtures("clear_db")
def test_create_subscription(authenticated_client: TestClient):
    response = authenticated_client.post(
        "/web/subscriptions/",
        content=json.dumps(
            {
                "webhook_url": "http://example.com/webhook",
                "feed_url": f"{FAKE_SERVER_URL}/abcnews_usheadlines.xml",
            }
        ),
    )
    assert response.status_code == 201
    response = response.json()
    assert response["id"] is not None
    assert response["inserted_at"] is not None

@pytest.mark.usefixtures("clear_db")
def test_try_create_subscription_with_invalid_data(authenticated_client: TestClient):
    response = authenticated_client.post(
        "/web/subscriptions/",
        content=json.dumps(
            {
                "webhook_url": "no-a-url",
                "feed_url": "",
            }
        ),
    )
    assert response.status_code == 422
    response = response.json()
    assert response["detail"]["webhook_url"] == ["invalid or missing URL scheme"]
    assert response["detail"]["feed_url"] == [
        "ensure this value has at least 1 characters"
    ]

@pytest.mark.usefixtures("clear_db")
def test_list_subscription(authenticated_client: TestClient):
    response = authenticated_client.get("/web/subscriptions/")
    assert response.status_code == 200
    response = response.json()
    assert response == []

@pytest.mark.usefixtures("clear_db")
def test_delete_subscription(authenticated_client: TestClient):
    response = authenticated_client.post(
        "/web/subscriptions/",
        content=json.dumps(
            {
                "webhook_url": "http://example.com/webhook",
                "feed_url": f"{FAKE_SERVER_URL}/abcnews_usheadlines.xml",
            }
        ),
    )
    assert response.status_code == 201
    response = response.json()
    subscription_id = response["id"]

    # Check if existent
    response = authenticated_client.get(
        f"/web/subscriptions/{subscription_id}",
    )
    assert response.status_code == 200

    # Delete
    response = authenticated_client.delete(
        f"/web/subscriptions/{subscription_id}",
    )
    assert response.status_code == 204

    # Check if still existent
    response = authenticated_client.get(
        f"/web/subscriptions/{subscription_id}",
    )
    assert response.status_code == 404

@pytest.mark.usefixtures("clear_db")
def test_try_delete_non_existent_subscription(authenticated_client: TestClient):
    subscription_id = 123
    response = authenticated_client.delete(
        f"/web/subscriptions/{subscription_id}",
    )
    assert response.status_code == 404

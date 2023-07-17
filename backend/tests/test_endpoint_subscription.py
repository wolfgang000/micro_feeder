import json
import os
from fastapi.testclient import TestClient
from backend.main import app
from .helper import create_authenticated_client

FAKE_SERVER_URL = os.getenv("FAKE_SERVER_URL")


def test_create_subscription():
    client = create_authenticated_client()
    response = client.post(
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


def test_try_create_subscription_with_invalid_data():
    client = create_authenticated_client()
    response = client.post(
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


def test_list_subscription():
    client = create_authenticated_client()
    response = client.get("/web/subscriptions/")
    assert response.status_code == 200
    response = response.json()
    assert response == []


def test_delete_subscription():
    client = create_authenticated_client()
    response = client.post(
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
    response = client.get(
        f"/web/subscriptions/{subscription_id}",
    )
    assert response.status_code == 200

    # Delete
    response = client.delete(
        f"/web/subscriptions/{subscription_id}",
    )
    assert response.status_code == 204

    # Check if still existent
    response = client.get(
        f"/web/subscriptions/{subscription_id}",
    )
    assert response.status_code == 404


def test_try_delete_non_existent_subscription():
    client = create_authenticated_client()
    subscription_id = 123
    response = client.delete(
        f"/web/subscriptions/{subscription_id}",
    )
    assert response.status_code == 404

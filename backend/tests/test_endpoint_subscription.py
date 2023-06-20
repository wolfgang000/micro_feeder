import json
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_create_subscription():
    response = client.post(
        "/web/subscriptions/",
        content=json.dumps(
            {
                "webhook_url": "http://example.com/webhook",
                "feed_url": "http://example.com/rss",
            }
        ),
    )
    assert response.status_code == 201
    response = response.json()
    assert response["id"] is not None


def test_try_create_subscription_with_invalid_data():
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
    assert response["detail"][0]["msg"] == "invalid or missing URL scheme"
    assert response["detail"][1]["msg"] == "ensure this value has at least 1 characters"

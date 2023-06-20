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

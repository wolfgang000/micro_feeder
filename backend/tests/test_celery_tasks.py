import json
import os
from backend.celery import tasks
from fastapi.testclient import TestClient
from backend.main import app
from backend.core import services
from fastapi.responses import FileResponse
from backend.core import models, unit_of_work
from .helper import create_authenticated_client

FAKE_SERVER_URL = os.getenv("FAKE_SERVER_URL")


def test_fetch_feed_with_new_items(monkeypatch):
    client = create_authenticated_client()
    response = client.post(
        "/web/subscriptions/",
        content=json.dumps(
            {
                "webhook_url": "http://testserver/",
                "feed_url": f"{FAKE_SERVER_URL}/abcnews_usheadlines_new_items.xml",
            }
        ),
    )
    subscription = response.json()

    def mock_return(webhook_url, payload):
        subscription_id = payload["subscription_id"]
        new_entries = payload["new_entries"]
        assert webhook_url == "http://testserver/"
        assert subscription_id == subscription["id"]
        assert len(new_entries) == 2
        first_entry = new_entries[0]
        assert first_entry == {
            "id": "https://abcnews.go.com/US/wireStory/mikala-jones-hawaii-surfer-filming-inside-waves-dies-101100274",
            "link": "https://abcnews.go.com/US/wireStory/mikala-jones-hawaii-surfer-filming-inside-waves-dies-101100274",
            "published_at": "Tue, 11 Jul 2023 21:42:24 -0400",
            "title": "Mikala Jones, Hawaii surfer known for filming inside waves, dies in surfing accident",
            "summary": "A Hawaii surfer known for shooting awe-inspiring photos and videos from the inside of massive, curling waves has died after a surfing accident in Indonesia",
        }

        return

    monkeypatch.setattr("backend.celery.tasks.call_webhook.delay", mock_return)

    tasks.fetch_feed(
        subscription_id=subscription["id"],
        feed_url=subscription["feed_url"],
        feed_last_entry_id="https://abcnews.go.com/US/wireStory/alabama-senator-white-nationalists-racists-after-weeks-declining-101113701",
        feed_last_etag="test",
        feed_last_modified="123",
        webhook_url=subscription["webhook_url"],
    )

    new_feed_last_entry_id = "https://abcnews.go.com/US/wireStory/mikala-jones-hawaii-surfer-filming-inside-waves-dies-101100274"

    response = client.get(f"/web/subscriptions/{subscription['id']}")
    updated_subscription = response.json()
    assert updated_subscription["feed_last_entry_id"] == new_feed_last_entry_id
    assert updated_subscription["feed_last_etag"] == None

from backend.core import serializers
from .main import app
import asyncio
from backend.core import unit_of_work, services
import httpx
import feedparser


@app.task
def fetch_feed(subscription_id, feed_url, feed_last_entry_id, webhook_url):
    feed = feedparser.parse(feed_url)
    entries = feed["entries"]

    new_feed_last_entry_id = entries[0]["id"]
    if new_feed_last_entry_id != feed_last_entry_id:
        entries_iter = iter(entries)
        new_entries = []
        while (entry := next(entries_iter, None)) is not None and entry[
            "id"
        ] != feed_last_entry_id:
            entry_serialized = serializers.FeedEntryWebhookRequest(
                id=entry["id"], link=entry["link"], summary=entry["summary"]
            )
            new_entries.append(entry_serialized.dict())

        payload = {"new_entries": new_entries}
        call_webhook.delay(webhook_url, payload)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            update_feed_last_entry_id(subscription_id, new_feed_last_entry_id)
        )


@app.task
def call_webhook(webhook_url, payload):
    httpx.post(webhook_url, json=payload)


@app.task
def schedule_fetch_feeds():
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(
        services.list_subscriptions(unit_of_work.SqlAlchemyUnitOfWork())
    )
    for item in result:
        fetch_feed.delay(
            item.id, item.feed_url, item.feed_last_entry_id, item.webhook_url
        )


async def update_feed_last_entry_id(id, feed_last_entry_id):
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    async with uow:
        await uow.subscription_repo.update_by_id(
            id, {"feed_last_entry_id": feed_last_entry_id}
        )
        await uow.commit()

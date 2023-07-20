from datetime import datetime, timezone, timedelta
from typing import Optional
import uuid
from backend.core import serializers
from backend.core.utils import download_feed_file
from result import Ok, Result, Err
from .main import app
import asyncio
from backend.core import unit_of_work, services
import httpx
import feedparser


@app.task
def fetch_feed(
    subscription_id,
    feed_url: str,
    feed_last_entry_id: str,
    feed_last_etag: str,
    feed_last_modified: str,
    webhook_url: str,
):
    loop = asyncio.get_event_loop()
    download_file_result = download_feed_file(
        feed_url, etag=feed_last_etag, last_modified=feed_last_modified
    )

    if isinstance(download_file_result, Err):
        loop.run_until_complete(
            update_subscription(
                subscription_id,
                {
                    "feed_last_fetched_at": datetime.now(timezone.utc),
                },
            )
        )
        return

    (file_path, new_etag, new_last_modified) = download_file_result.ok_value

    feed = feedparser.parse(file_path)

    if feed["bozo"]:
        loop.run_until_complete(
            update_subscription(
                subscription_id,
                {
                    "feed_last_fetched_at": datetime.now(timezone.utc),
                },
            )
        )
        return

    entries = feed["entries"]
    new_feed_last_entry_id = entries[0]["id"]
    if new_feed_last_entry_id != feed_last_entry_id:
        entries_iter = iter(entries)
        new_entries = []
        while (entry := next(entries_iter, None)) is not None and entry[
            "id"
        ] != feed_last_entry_id:
            entry_serialized = serializers.FeedEntryWebhookRequest(
                id=entry.get("id"),
                link=entry.get("link"),
                title=entry.get("title"),
                summary=entry.get("summary"),
                published_at=entry.get("published"),
            )
            new_entries.append(entry_serialized.dict())

        payload = {"subscription_id": subscription_id, "new_entries": new_entries}
        call_webhook.delay(webhook_url, payload)

        loop.run_until_complete(
            update_subscription(
                subscription_id,
                {
                    "feed_last_entry_id": new_feed_last_entry_id,
                    "feed_last_etag": new_etag,
                    "feed_last_modified": new_last_modified,
                    "feed_last_fetched_at": datetime.now(timezone.utc),
                },
            )
        )
    else:
        loop.run_until_complete(
            update_subscription(
                subscription_id,
                {
                    "feed_last_fetched_at": datetime.now(timezone.utc),
                },
            )
        )
    return


@app.task
def call_webhook(webhook_url, payload):
    httpx.post(webhook_url, json=payload)


@app.task
def schedule_fetch_feeds():
    result = services.list_pending_to_feach_subscriptions(
        unit_of_work.SqlAlchemyUnitOfWork(),
        datetime.now(timezone.utc) + timedelta(minutes=-5),
    )

    for item in result:
        fetch_feed.delay(
            item.id,
            item.feed_url,
            item.feed_last_entry_id,
            item.feed_last_etag,
            item.feed_last_modified,
            item.webhook_url,
        )


async def update_subscription(subscription_id, params):
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    async with uow:
        await uow.subscription_repo.update_by_id(subscription_id, params)
        await uow.commit()

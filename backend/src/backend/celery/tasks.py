from typing import Optional
import uuid
from backend.core import serializers
from result import Ok, Result, Err
from .main import app
import asyncio
from backend.core import unit_of_work, services
import httpx
import feedparser

ACCEPT_HEADER: str = (
    "application/atom+xml"
    ",application/rdf+xml"
    ",application/rss+xml"
    ",application/x-netcdf"
    ",application/xml"
    ";q=0.9,text/xml"
    ";q=0.2,*/*"
    ";q=0.1"
)


def download_file(
    url: str, etag: Optional[str], last_modified: Optional[str]
) -> Result[str, str]:
    temp_file_name = f"/tmp/{uuid.uuid4()}"
    headers = {"Accept": ACCEPT_HEADER}

    if etag:
        headers["If-None-Match"] = etag

    if last_modified:
        headers["If-Modified-Since"] = last_modified

    responce = httpx.get(url, headers=headers)

    if responce.status_code == 304:
        return Err("Not Modified")

    # Some times the servers has the Last-Modified header but doesn't implement the If-Modified-Since validation logic
    if responce.headers.get("Last-Modified") == last_modified:
        return Err("Not Modified")

    if responce.status_code == 200:
        with open(temp_file_name, "wb") as f:
            f.write(responce.content)
        return Ok(temp_file_name)
    else:
        return Err(f"Error: {responce.status_code}")


@app.task
def fetch_feed(
    subscription_id,
    feed_url: str,
    feed_last_entry_id: str,
    feed_last_etag: str,
    feed_last_modified: str,
    webhook_url: str,
):
    download_file_result = download_file(
        feed_url, etag=feed_last_etag, last_modified=feed_last_modified
    )

    if isinstance(download_file_result, Err):
        return

    file_path = download_file_result.ok_value

    feed = feedparser.parse(file_path)

    if feed["bozo"]:
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
                id=entry["id"], link=entry["link"], summary=entry["summary"]
            )
            new_entries.append(entry_serialized.dict())

        payload = {"new_entries": new_entries}
        call_webhook.delay(webhook_url, payload)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            update_subscription(
                subscription_id,
                {
                    "feed_last_entry_id": new_feed_last_entry_id,
                    "feed_last_etag": feed.get("etag"),
                    "feed_last_modified": feed.get("modified"),
                },
            )
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

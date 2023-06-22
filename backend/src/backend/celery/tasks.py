from .main import app
import asyncio
from celery.schedules import crontab
from backend.core import unit_of_work, services
import feedparser


@app.task
def test(arg):
    print(arg)


@app.task
def add(x, y):
    z = x + y
    print(z)
    return z


@app.task
def mul(x, y):
    return x * y


@app.task
def fetch_feed_and_call_webhook(
    subscription_id, feed_url, feed_last_entry_id, webhook_url
):
    feed = feedparser.parse(feed_url)


@app.task
def schedule_fetch_feeds():
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(get_suscription_list())
    for (item,) in result:
        fetch_feed_and_call_webhook.delay(
            item.id, item.feed_url, item.feed_last_entry_id, item.webhook_url
        )


async def foo():
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    result = await services.get_db_health_status(uow)
    return result


async def get_suscription_list():
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    async with uow:
        result = await uow.subscription_repo.list()
        return list(result)

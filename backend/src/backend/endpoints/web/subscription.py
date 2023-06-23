from __future__ import annotations
import uuid
from backend.core.utils import download_feed_file
from fastapi import APIRouter, Response, status
from backend.core import unit_of_work, services, serializers
from httpx import AsyncClient
import aiofiles


router = APIRouter()


@router.post("/web/subscriptions/", status_code=201)
async def create_subscription(subscriptionRequest: serializers.SubscriptionRequest):
    await download_feed_file(subscriptionRequest.feed_url)
    # async with AsyncClient() as client:
    #     async with client.stream('GET', subscriptionRequest.feed_url) as response:
    #         async for chunk in response.aiter_bytes():
    # async with AsyncClient() as client:
    #     result = await client.get(subscriptionRequest.feed_url)
    #     if result.status_code == 200:
    #         temp_file_name = f"/tmp/{uuid.uuid4()}"
    #         async with aiofiles.open(temp_file_name, mode="wb") as f:
    #             await f.write(result.content)
    #     else:
    #         return None

    uow = unit_of_work.SqlAlchemyUnitOfWork()
    subscription = await services.create_subscription(uow, subscriptionRequest.dict())
    return subscription

from __future__ import annotations
from backend.core.utils import download_feed_file
from fastapi import APIRouter, HTTPException, Response, status
from backend.core import unit_of_work, services, serializers

router = APIRouter()


@router.post("/web/subscriptions/", status_code=201)
async def create_subscription(subscriptionRequest: serializers.SubscriptionRequest):
    result = await download_feed_file(subscriptionRequest.feed_url)
    if result.is_err():
        raise HTTPException(status_code=422, detail="Item not found")

    uow = unit_of_work.SqlAlchemyUnitOfWork()
    subscription = await services.create_subscription(uow, subscriptionRequest.dict())
    return subscription

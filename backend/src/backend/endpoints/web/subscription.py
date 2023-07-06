from __future__ import annotations
from backend.core.utils import download_feed_file
from fastapi import APIRouter, HTTPException, Response, status
from backend.core import unit_of_work, services, serializers

router = APIRouter()


@router.post("/web/subscriptions/", status_code=201)
async def create_subscription(subscriptionRequest: serializers.SubscriptionRequest):
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    subscription = await services.create_subscription(uow, subscriptionRequest.dict())
    return subscription


@router.get("/web/subscriptions/", status_code=200)
async def list_subscription():
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    subscriptions = await services.list_subscriptions(uow)
    return subscriptions

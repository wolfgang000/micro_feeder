from __future__ import annotations
from fastapi import APIRouter, Response, status
from backend.core import unit_of_work, services, serializers

router = APIRouter()


@router.post("/web/subscriptions/", status_code=201)
async def create_subscription(subscriptionRequest: serializers.SubscriptionRequest):
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    subscription = await services.create_subscription(uow, subscriptionRequest.dict())
    return subscription

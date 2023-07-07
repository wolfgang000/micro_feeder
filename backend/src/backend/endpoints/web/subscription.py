from __future__ import annotations
from typing import Annotated
from backend.auth import get_current_user
from backend.core.utils import download_feed_file
from fastapi import APIRouter, Depends, HTTPException, Response, status
from backend.core import models, unit_of_work, services, serializers

router = APIRouter()


@router.post("/web/subscriptions/", status_code=201)
async def create_subscription(
    subscriptionRequest: serializers.SubscriptionRequest,
    current_user: Annotated[models.User, Depends(get_current_user)],
):
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    subscription = await services.create_subscription(
        uow, {**subscriptionRequest.dict(), "user_id": current_user.id}
    )
    return subscription


@router.get("/web/subscriptions/", status_code=200)
async def list_subscription(
    current_user: Annotated[models.User, Depends(get_current_user)],
):
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    subscriptions = await services.list_subscriptions_by_user_id(uow, current_user.id)
    return subscriptions

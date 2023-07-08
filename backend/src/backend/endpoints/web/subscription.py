from __future__ import annotations
from typing import Annotated
from backend.auth import get_current_user
from backend.core.utils import download_feed_file
from fastapi import APIRouter, Depends, HTTPException, Response, status
from backend.core import models, unit_of_work, services, serializers
from result import Err

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


@router.get("/web/subscriptions/{subscription_id}", status_code=200)
async def get_subscription(
    subscription_id: int,
    current_user: Annotated[models.User, Depends(get_current_user)],
    response: Response,
):
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    get_subscription_by_id_and_user_id_result = (
        await services.get_subscription_by_id_and_user_id(
            uow, current_user.id, subscription_id
        )
    )

    if isinstance(get_subscription_by_id_and_user_id_result, Err):
        response.status_code = status.HTTP_404_NOT_FOUND
        return

    subscription = get_subscription_by_id_and_user_id_result.ok_value
    return subscription


@router.delete("/web/subscriptions/{subscription_id}", status_code=204)
async def delete_subscription(
    subscription_id: int,
    current_user: Annotated[models.User, Depends(get_current_user)],
    response: Response,
):
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    get_subscription_by_id_and_user_id_result = (
        await services.get_subscription_by_id_and_user_id(
            uow, current_user.id, subscription_id
        )
    )

    if isinstance(get_subscription_by_id_and_user_id_result, Err):
        response.status_code = status.HTTP_404_NOT_FOUND
        return

    await services.delete_subscription_by_id(uow, subscription_id)
    return

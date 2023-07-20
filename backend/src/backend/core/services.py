import datetime
from backend.core import unit_of_work, models
from result import Ok, Err, Result
from sqlalchemy.sql import text
from sqlalchemy import select
from typing import Any


# TODO: Add proper loggers and better error messages


async def get_db_health_status(uow: unit_of_work.SqlAlchemyUnitOfWork) -> Result:
    try:
        async with uow:
            result = await uow.session.execute(text("SELECT 1"))
            match list(result):
                case [(1,)]:
                    return Ok[Any](None)
                case value:
                    print(f"Error, expected [(1,)] but got {value}")
                    return Err(value)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return Err(err)


async def create_subscription(
    uow: unit_of_work.SqlAlchemyUnitOfWork, subscription_params: dict
) -> models.Subscription:
    async with uow:
        subscription = await uow.subscription_repo.create(
            models.Subscription(**subscription_params)
        )
        await uow.commit()
        return subscription


async def list_subscriptions_by_user_id(
    uow: unit_of_work.SqlAlchemyUnitOfWork, user_id: int
) -> list[models.Subscription]:
    async with uow:
        result = await uow.subscription_repo.list_by_user_id(user_id)
        subscriptions = [r for (r,) in list(result)]
        return subscriptions


async def list_subscriptions(
    uow: unit_of_work.SqlAlchemyUnitOfWork,
) -> list[models.Subscription]:
    async with uow:
        result = await uow.subscription_repo.list()
        subscriptions = [r for (r,) in list(result)]
        return subscriptions


def list_pending_to_feach_subscriptions(
    uow: unit_of_work.SqlAlchemyUnitOfWork,
    from_date: datetime.datetime,
) -> list[models.Subscription]:
    with uow:
        result = uow.sync_session.execute(
            select(models.Subscription).where(
                models.Subscription.feed_last_fetched_at > from_date
            )
        )
        subscriptions = [r for (r,) in list(result)]
        return subscriptions


async def get_subscription_by_id_and_user_id(
    uow: unit_of_work.SqlAlchemyUnitOfWork,
    user_id: int,
    subscription_id: int,
):
    async with uow:
        result = await uow.subscription_repo.get_by_id_and_user_id(
            subscription_id, user_id
        )
        return result


async def delete_subscription_by_id(
    uow: unit_of_work.SqlAlchemyUnitOfWork,
    subscription_id: int,
):
    async with uow:
        await uow.subscription_repo.delete_by_id(subscription_id)
        await uow.commit()


async def create_user(
    uow: unit_of_work.SqlAlchemyUnitOfWork, user_params: dict
) -> models.User:
    async with uow:
        # TODO: handle unique constrain error
        user = await uow.user_repo.create(models.User(**user_params))
        await uow.commit()
        return user

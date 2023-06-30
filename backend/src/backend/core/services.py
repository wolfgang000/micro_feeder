from backend.core import unit_of_work, models
from result import Ok, Err, Result
from sqlalchemy.sql import text

# TODO: Add proper loggers and better error messages


async def get_db_health_status(uow: unit_of_work.SqlAlchemyUnitOfWork) -> Result:
    try:
        async with uow:
            result = await uow.session.execute(text("SELECT 1"))
            match list(result):
                case [(1,)]:
                    return Ok()
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


async def create_user(
    uow: unit_of_work.SqlAlchemyUnitOfWork, user_params: dict
) -> models.User:
    async with uow:
        # TODO: handle unique constrain error
        user = await uow.user_repo.create(models.User(**user_params))
        await uow.commit()
        return user

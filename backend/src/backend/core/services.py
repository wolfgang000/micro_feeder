from backend.core import unit_of_work
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

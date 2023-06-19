from backend.core import unit_of_work
from result import Ok, Err, Result
from sqlalchemy.sql import text


async def get_db_health_status(uow: unit_of_work.SqlAlchemyUnitOfWork) -> Result:
    try: 
        async with uow:
            result = await uow.session.execute(text('SELECT 1'))
            print(list(results))
            return Ok()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return Err(err)

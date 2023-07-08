from typing import Annotated
from backend.core import models, unit_of_work
from fastapi import Depends, HTTPException, Request, status
from result import Ok


async def get_current_user(request: Request) -> models.User:
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    uow = unit_of_work.SqlAlchemyUnitOfWork()
    async with uow:
        get_by_id_result = await uow.user_repo.get_by_id(user_id)

    if isinstance(get_by_id_result, Ok):
        user = get_by_id_result.ok_value
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

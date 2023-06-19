
from __future__ import annotations
from fastapi import APIRouter
from backend.core import unit_of_work
from sqlalchemy.sql import text


router = APIRouter()

@router.get("/api/health")
async def get_health():
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    async with uow:
        results = await uow.session.execute(text('SELECT 1'))
        print(results)

    return "ok"
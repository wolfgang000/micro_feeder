
from __future__ import annotations
from fastapi import APIRouter, Response, status
from backend.core import unit_of_work, services

router = APIRouter()

@router.get("/api/health")
async def get_health(response: Response):
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    result = await services.get_db_health_status(uow)
    postgre_status = result.map_or_else(lambda: {"name": "PostgreSQL", "status": "unhealthy"}, lambda _x: {"name": "PostgreSQL", "status": "healthy"})
    checks = [ postgre_status ]
    if any(check["status"] == "unhealthy" for check in checks):
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return checks
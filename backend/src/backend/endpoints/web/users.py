from typing import Annotated
from backend.core import models
from backend.auth import get_current_user
from fastapi import APIRouter, Depends, HTTPException, Response, status

router = APIRouter()


@router.get("/web/users/me/", status_code=200)
async def list_subscription(
    current_user: Annotated[models.User, Depends(get_current_user)],
):
    return current_user

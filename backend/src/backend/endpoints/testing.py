from backend.config import Config
from backend.core import unit_of_work
from backend.core.services import create_user
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

router = APIRouter()


@router.get("/testing/create_user_and_login/")
async def logout(request: Request, user_email: str):
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    user = await create_user(uow, {"email": user_email})
    request.session.update({"user_id": user.id})
    return RedirectResponse(f"{Config.FRONTEND_URL}/subscriptions")

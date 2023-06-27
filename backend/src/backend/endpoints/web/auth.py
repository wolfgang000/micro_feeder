from backend.config import Config
from backend.core import unit_of_work
from backend.core.services import create_user
from fastapi import APIRouter, Request
from oauthlib.oauth2 import WebApplicationClient
from fastapi.responses import RedirectResponse
from httpx import AsyncClient
from result import Err, Ok, Result


router = APIRouter()


class GoogleOAuth:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        token_uri: str = "https://oauth2.googleapis.com/token",
        authorize_url: str = "https://accounts.google.com/o/oauth2/auth",
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.token_uri = token_uri
        self.authorize_url = authorize_url
        self.client = WebApplicationClient(client_id)

    def get_authorization_url(self):
        return self.client.prepare_request_uri(
            self.authorize_url,
            redirect_uri=self.redirect_uri,
            scope="https://www.googleapis.com/auth/userinfo.email",
        )

    async def fetch_token(self, code) -> Result[dict, str]:
        body = self.client.prepare_request_body(
            code=code, redirect_uri=self.redirect_uri, client_secret=self.client_secret
        )
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        async with AsyncClient() as client:
            result = await client.post(
                self.token_uri,
                content=body,
                headers=headers,
            )
            if result.status_code == 200:
                return Ok(result.json())
            else:
                return Err(result.text)


client = GoogleOAuth(
    client_id=Config.GOOGLE_CLIENT_ID,
    client_secret=Config.GOOGLE_CLIENT_SECRET,
    redirect_uri=Config.GOOGLE_REDIRECT_URI,
)


async def get_account_info(access_token) -> Result[dict, str]:
    async with AsyncClient() as client:
        result = await client.get(
            f"https://www.googleapis.com/oauth2/v1/userinfo?access_token={access_token}"
        )
        if result.status_code == 200:
            return Ok(result.json())
        else:
            return Err(result.text)


@router.get("/web/auth/login")
async def login(request: Request):
    user_id = request.session.get("user_id")
    redirect_url = (
        f"{Config.FRONTEND_URL}/dashboard"
        if user_id
        else client.get_authorization_url()
    )
    return RedirectResponse(redirect_url)


@router.get("/web/auth/callback")
async def callback(request: Request, code: str):
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    fetch_token_result = await client.fetch_token(code)

    if isinstance(fetch_token_result, Ok):
        access_token = fetch_token_result.value["access_token"]
        account_info_result = await get_account_info(access_token)
        if isinstance(account_info_result, Ok):
            user_email = account_info_result.value["email"]

            async with uow:
                get_user_by_email_result = await uow.user_repo.get_by_email(user_email)

            if isinstance(get_user_by_email_result, Ok):
                user = get_user_by_email_result.value
                request.session.update({"user_id": user.id})

                return "ok"
            else:
                user = await create_user(uow, {"email": user_email})
                request.session.update({"user_id": user.id})

                return "ok"
        else:
            pass
    else:
        pass


@router.post("/web/auth/logout")
async def logout(request: Request):
    request.session.clear()
    return "ok"

from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends

from src.auth.authentication import authenticate_user, create_access_token
from src.schemas.auth import Token
from src.shared.dependencies import AsyncSessionAnnotated
from src.shared.base_config import settings
from src.shared.exceptions import InvalidCredentialsError

router = APIRouter()


@router.get("/health")
async def healthcheck():
    return {"status": "ok"}


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSessionAnnotated,
) -> Token:
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise InvalidCredentialsError()
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user": user.username, "role": user.role},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")

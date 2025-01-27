import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import DatabaseError, InternalError
from jwt.exceptions import InvalidTokenError
from typing import Annotated
from pydantic import ValidationError

from src.models.model import User
from src.shared.base_config import settings
from src.shared.db import get_async_session
from src.shared.exceptions import CredentialsValidationError, GenericDatabaseError, InsufficientPermissionsError
from src.schemas.user import UserCreds, UserCredsDB

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="fake/token",
    scopes={"user": "Base user access", "admin": "Admin limited access"},
)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user(session: AsyncSession, username: str):
    try:
        query = select(User).where(User.username == username)
        user = (await session.execute(query)).scalar_one_or_none()
        if user:
            return UserCredsDB(**user.__dict__)
    except (DatabaseError, InternalError):
        raise GenericDatabaseError()


async def authenticate_user(session: AsyncSession, username: str, password: str):
    user = await get_user(session, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


async def get_current_user(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("user")
        if username is None:
            raise CredentialsValidationError(authenticate_value)
        user_role = payload.get("role", None)
    except (InvalidTokenError, ValidationError):
        raise CredentialsValidationError(authenticate_value)
    user = await get_user(session, username)
    if user is None:
        raise CredentialsValidationError(authenticate_value)
    if security_scopes.scopes:
        if not user_role or user_role not in security_scopes.scopes:
            raise InsufficientPermissionsError(authenticate_value)
    return UserCreds(**user.model_dump())

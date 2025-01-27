from fastapi import APIRouter
from sqlalchemy import select

from src.models.model import User
from src.schemas.user import UserCreds
from src.shared.dependencies import (
    AsyncSessionAnnotated,
    CurrentAdminRole,
    CurrentUser,
    CurrentUserRole
)
from src.shared.exceptions import GenericDatabaseError

router = APIRouter()


@router.get("/current_user", response_model=UserCreds, response_model_by_alias=False)
async def current_user(
    current_user: CurrentUser,
):
    return current_user

@router.get("/all", response_model=list[UserCreds], response_model_by_alias=False)
async def get_all_users(session: AsyncSessionAnnotated, _: CurrentAdminRole):
    try:
        query = select(User.role, User.username)
        return await session.execute(query)
    except Exception as e:
        raise GenericDatabaseError()

@router.get("/users", response_model=list[UserCreds], response_model_by_alias=False)
async def get_all_user_roles(session: AsyncSessionAnnotated, _: CurrentUserRole):
    try:
        query = select(User.role, User.username).where(User.role == "user")
        return await session.execute(query)
    except Exception as e:
        raise GenericDatabaseError()

@router.get("/admins", response_model=list[UserCreds], response_model_by_alias=False)
async def get_all_admin_roles(session: AsyncSessionAnnotated, _: CurrentAdminRole):
    try:
        query = select(User.role, User.username).where(User.role == "admin")
        return await session.execute(query)
    except Exception as e:
        raise GenericDatabaseError()

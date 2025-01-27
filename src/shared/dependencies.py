from typing import Annotated

from fastapi import Depends, Security
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.db import get_async_session
from src.schemas.user import UserCreds
from src.auth.authentication import get_current_user

AsyncSessionAnnotated = Annotated[AsyncSession, Depends(get_async_session)]
CurrentUser = Annotated[UserCreds, Security(get_current_user, scopes=[])]
CurrentUserRole = Annotated[UserCreds, Security(get_current_user, scopes=["user"])]
CurrentAdminRole = Annotated[UserCreds, Security(get_current_user, scopes=["admin"])]

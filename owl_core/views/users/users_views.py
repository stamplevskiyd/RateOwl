from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from owl_core.daos.dependencies import get_dao_factory
from owl_core.api.schemas import Token
from owl_core.daos.user_dao import UserDAO
from owl_core.models.users import User
from owl_core.users.utils import authenticate_user, create_access_token

users_router = APIRouter(prefix="/users", tags=["Users"])

UserDAODep = Annotated[UserDAO, Depends(get_dao_factory(UserDAO))]


@users_router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], user_dao: UserDAODep
) -> Token:
    """Login by access token"""
    user: User | None = await authenticate_user(
        form_data.username, form_data.password, user_dao
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")

from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from owl_core.api.users.dependencies import get_current_active_user
from owl_core.api.users.utils import (
    authenticate_user,
    create_access_token,
    get_password_hash,
)
from owl_core.daos.dependencies import get_dao_factory
from owl_core.api.schemas import Token
from owl_core.daos.user_dao import UserDAO
from owl_core.models.users import User
from owl_core.schemas.users import UserPost, UserGet

users_router = APIRouter(prefix="/users", tags=["Users"])

UserDAODep = Annotated[UserDAO, Depends(get_dao_factory(UserDAO))]


# TODO: this is not an api. move to views or somewhere else
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


@users_router.post("/add", status_code=status.HTTP_201_CREATED, response_model=UserGet)
async def add_user(user: UserPost, user_dao: UserDAODep) -> User:
    user_data = user.model_dump()
    del user_data["password"]
    user_data["hashed_password"] = get_password_hash(user.password)
    return await user_dao.create(user_data)


@users_router.get("/", response_model=list[UserGet])
async def get_users(user_dao: UserDAODep) -> list[User]:
    return await user_dao.find_all()


@users_router.get("/me", response_model=UserGet)
async def get_current_user_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> User:
    return current_user

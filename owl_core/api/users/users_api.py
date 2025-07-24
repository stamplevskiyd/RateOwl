from typing import Annotated

from fastapi import APIRouter, status, Depends

from owl_core.api.users.dependencies import get_current_user
from owl_core.daos.dependencies import get_dao_factory
from owl_core.daos.user_dao import UserDAO
from owl_core.models.users import User
from owl_core.schemas.users import UserPost, UserGet
from owl_core.users.utils import get_password_hash

users_router = APIRouter(prefix="/users", tags=["Users"])

UserDAODep = Annotated[UserDAO, Depends(get_dao_factory(UserDAO))]


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
async def get_user_me(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    return current_user

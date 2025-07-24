from typing import Annotated

from fastapi import Depends, HTTPException
from starlette import status
from owl_core.context import current_username, current_user_id
from owl_core.daos.dependencies import get_dao_factory
from owl_core.daos.user_dao import UserDAO
from owl_core.models.users import User

UserDAODep = Annotated[UserDAO, Depends(get_dao_factory(UserDAO))]

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_current_user(user_dao: UserDAODep) -> User:
    username = current_username.get()
    if not username:
        raise credentials_exception
    user = await user_dao.find_by_username_or_email(username)
    if not user:
        raise credentials_exception
    current_user_id.set(user.id)
    return user


async def get_current_user_or_none(
    user_dao: UserDAODep,
) -> User | None:
    try:
        return await get_current_user(user_dao)
    except HTTPException:
        return None

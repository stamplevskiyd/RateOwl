from typing import Annotated, Awaitable, Callable

import jwt
from fastapi import Depends, HTTPException
from jwt import InvalidTokenError
from starlette import status

from owl_core.api.users.utils import oauth2_scheme
from owl_core.config import settings
from owl_core.daos.dependencies import get_dao_factory
from owl_core.daos.user_dao import UserDAO
from owl_core.models.users import User

UserDAODep = Annotated[UserDAO, Depends(get_dao_factory(UserDAO))]

# TODO: move all to config
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"


def user_get_factory(
    raise_exception: bool = False,
) -> Callable[[str, UserDAO], Awaitable[User | None]]:
    async def get_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        user_dao: UserDAODep,
    ) -> User | None:
        """Get current authenticated user"""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                username = payload.get("sub")
                if not username:
                    raise credentials_exception
            except InvalidTokenError:
                raise credentials_exception
            user = await user_dao.find_by_username_or_email(username)
            if user is None:
                raise credentials_exception
            return user
        except HTTPException:
            if raise_exception:
                raise
            return None

    return get_user


get_current_user = user_get_factory(raise_exception=True)
get_current_user_optional = user_get_factory(raise_exception=False)


async def get_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if not current_user.active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_active_user_or_none(
    current_user: Annotated[User | None, Depends(get_current_user_optional)],
) -> User | None:
    if current_user and not current_user.active:
        return None
    return current_user

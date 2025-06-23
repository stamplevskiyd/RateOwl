from typing import Annotated

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


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], user_dao: UserDAODep
) -> User:
    """Get current authenticated user"""
    # TODO: better exception
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
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


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if not current_user.active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

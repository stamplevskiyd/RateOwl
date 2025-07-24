from datetime import datetime, timezone, timedelta
from typing import Annotated, Any

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from passlib.context import CryptContext

from owl_core.config import settings
from owl_core.daos.dependencies import get_dao_factory
from owl_core.daos.user_dao import UserDAO
from owl_core.models.users import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
UserDAODep = Annotated[UserDAO, Depends(get_dao_factory(UserDAO))]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token", auto_error=False)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check if user's password is valid"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate a password hash"""
    return pwd_context.hash(password)


async def authenticate_user(
    username: str, password: str, user_dao: UserDAODep
) -> User | None:
    """User authentication check if user exists)"""
    user: User | None = await user_dao.find_by_username_or_email(username)
    if not user or not user.active:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict[str, Any]) -> str:
    """Generate access token for authenticated user"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


async def get_username(token: str) -> str | None:
    """Get username of current user"""
    token = token.split("Bearer")[1].strip()  # TODO: there surely is a better way
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username = payload.get("sub")
        if not username:
            return None
    except InvalidTokenError:
        return None
    return username

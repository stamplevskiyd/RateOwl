from typing import Annotated
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel

from owl_core.config import settings
from owl_core.daos.user_dao import UserDAO
from owl_core.db.session import SessionDep
from owl_core.models.users import User
from owl_core.schemas.users import UserPost, UserGet

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

users_router = APIRouter(prefix="/users", tags=["Users"])


async def get_user_dao(session: SessionDep) -> UserDAO:
    return UserDAO(session)


UserDAODep = Annotated[UserDAO, Depends(get_user_dao)]


class Token(BaseModel):
    access_token: str
    token_type: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/users/token")


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


def create_access_token(data: dict) -> str:
    """Generate access token for authenticated user"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: Annotated[Token, Depends(oauth2_scheme)], user_dao: UserDAODep
) -> User:
    """Get current authenticated user"""
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

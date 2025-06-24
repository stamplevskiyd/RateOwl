from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str | None = None


class UserGet(UserBase):
    id: int
    active: bool


class UserPost(UserBase):
    # password: SecretStr
    password: str

from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str | None = None


class UserGet(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    active: bool


class UserPost(UserBase):
    # password: SecretStr
    password: str

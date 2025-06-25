from pydantic import BaseModel

from owl_core.schemas.users import UserGet


class TagBase(BaseModel):
    name: str


class TagGet(TagBase):
    id: int
    author: UserGet


class TagPost(TagBase):
    pass

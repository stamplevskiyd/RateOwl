from pydantic import BaseModel

from owl_core.schemas.users import UserGet


class TagBase(BaseModel):
    name: str


class TagGet(TagBase):
    id: int
    created_by: UserGet


class TagPost(TagBase):
    pass

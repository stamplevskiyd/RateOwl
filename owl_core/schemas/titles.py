from pydantic import BaseModel

from owl_core.schemas.tags import TagGet
from owl_core.schemas.users import UserGet


class TitleBase(BaseModel):
    name: str


class TitleGet(TitleBase):
    id: int
    tags: list[TagGet]
    created_by: UserGet


class TitlePost(TitleBase):
    tags: list[int]


class TitlePut(TitlePost):
    pass

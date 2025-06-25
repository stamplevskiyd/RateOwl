from pydantic import BaseModel

from owl_core.schemas.tags import TagGet


class TitleBase(BaseModel):
    name: str


class TitleGet(TitleBase):
    id: int
    tags: list[TagGet]


class TitlePost(TitleBase):
    tags: list[int]


class TitlePut(TitlePost):
    pass

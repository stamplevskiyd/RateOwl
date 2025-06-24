from pydantic import BaseModel, ConfigDict

from owl_core.schemas.tags import TagGet


class TitleBase(BaseModel):
    name: str
    slug: str


class TitleGet(TitleBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    tags: list[TagGet]


class TitlePost(TitleBase):
    pass

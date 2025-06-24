import datetime

from pydantic import BaseModel, Field, ConfigDict

from owl_core.schemas.tags import TagGet, TagPost
from owl_core.schemas.titles import TitleGet
from owl_core.schemas.users import UserGet


class ReviewBase(BaseModel):
    description: str = Field(min_length=1, max_length=255)
    text: str
    rate: int = Field(ge=1, le=10)


class ReviewGet(ReviewBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    title: TitleGet
    author: UserGet
    tags: list[TagGet]


class ReviewPost(ReviewBase):
    title_id: int
    tags: list[TagPost] | None = None

class ReviewPut(ReviewPost):
    pass

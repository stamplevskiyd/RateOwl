import datetime

from pydantic import BaseModel, Field

from owl_core.schemas.tags import TagGet
from owl_core.schemas.titles import TitleGet
from owl_core.schemas.users import UserGet


class ReviewBase(BaseModel):
    # description: str = Field(min_length=1, max_length=255)
    text: str
    rate: int = Field(ge=1, le=10)
    hidden: bool = False


class ReviewGet(ReviewBase):
    id: int
    created_on: datetime.datetime
    changed_on: datetime.datetime
    title: TitleGet
    created_by: UserGet
    tags: list[TagGet]


class ReviewPost(ReviewBase):
    title_id: int


class ReviewPut(ReviewBase):
    pass

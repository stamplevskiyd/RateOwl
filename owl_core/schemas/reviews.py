import datetime

from pydantic import BaseModel, Field


class ReviewBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    rate: int = Field(ge=1, le=10)


class ReviewGet(ReviewBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime


class ReviewPost(ReviewBase):
    pass

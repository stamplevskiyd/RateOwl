from pydantic import BaseModel


class TitleBase(BaseModel):
    name: str
    slug: str


class TitleGet(TitleBase):
    id: int


class TitlePost(TitleBase):
    pass

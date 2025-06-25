from pydantic import BaseModel


class TagBase(BaseModel):
    name: str


class TagGet(TagBase):
    id: int


class TagPost(TagBase):
    pass

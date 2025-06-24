from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException

from owl_core.daos.dependencies import get_dao_factory
from owl_core.daos.tag_dao import TagDAO
from owl_core.models.tags import Tag
from owl_core.schemas.tags import TagPost, TagGet

tags_router = APIRouter(prefix="/tags", tags=["Tags"])

TagDAODep = Annotated[TagDAO, Depends(get_dao_factory(TagDAO))]


@tags_router.post("/add", status_code=status.HTTP_201_CREATED, response_model=TagGet)
async def add_tag(tag: TagPost, tag_dao: TagDAODep) -> Tag:
    tag = await tag_dao.create(tag.model_dump())
    return tag


@tags_router.post("/", response_model=list[TagGet])
async def get_tags(tag_dao: TagDAODep) -> list[Tag]:
    return await tag_dao.find_all()


@tags_router.get("/{tag_id}", response_model=TagGet)
async def get_tag(tag_id: int, tags_dao: TagDAODep) -> Tag:
    tag = await tags_dao.find_by_id(tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

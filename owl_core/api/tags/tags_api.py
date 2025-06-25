from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException

from owl_core.api.users.dependencies import get_current_active_user
from owl_core.commands.tags.create_tag import CreateTagCommand
from owl_core.commands.tags.update_tag import UpdateTagCommand
from owl_core.daos.dependencies import get_dao_factory
from owl_core.daos.tag_dao import TagDAO
from owl_core.models.tags import Tag
from owl_core.models.users import User
from owl_core.schemas.tags import TagPost, TagGet

tags_router = APIRouter(prefix="/tags", tags=["Tags"])

TagDAODep = Annotated[TagDAO, Depends(get_dao_factory(TagDAO))]


@tags_router.get(
    "/",
)
async def get_tags(tag_dao: TagDAODep) -> list[TagGet]:
    tags = await tag_dao.find_all()
    return [TagGet.model_validate(tag, from_attributes=True) for tag in tags]


@tags_router.get("/{tag_id}")
async def get_tag(tag_id: int, tags_dao: TagDAODep) -> TagGet:
    tag = await tags_dao.find_by_id(tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return TagGet.model_validate(tag, from_attributes=True)


@tags_router.post("/add", status_code=status.HTTP_201_CREATED, response_model=TagGet)
async def create_tag(
    tag: TagPost,
    current_user: Annotated[User, Depends(get_current_active_user)],
    tag_dao: TagDAODep,
) -> Tag:
    command = CreateTagCommand(tag, current_user, tag_dao)
    return await command.run()


@tags_router.put("/{tag_id}", response_model=TagGet)
async def update_tag(
    tag_id: int,
    tag: TagPost,
    current_user: Annotated[User, Depends(get_current_active_user)],
    tag_dao: TagDAODep,
) -> Tag:
    tag_object: Tag | None = await tag_dao.find_by_id(tag_id)

    if tag_object is None:
        raise HTTPException(status_code=404, detail="Tag not found")

    if tag_object.author != current_user:
        raise HTTPException(status_code=403, detail="You can only edit your own tags")

    command = UpdateTagCommand(tag_object, tag, current_user, tag_dao)
    updated_tag = await command.run()
    return updated_tag

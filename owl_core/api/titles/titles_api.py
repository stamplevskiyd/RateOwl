from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from owl_core.api.users.dependencies import get_current_active_user
from owl_core.commands.titles.create_title import CreateTitleCommand
from owl_core.commands.titles.update_title import UpdateTitleCommand
from owl_core.daos.dependencies import get_dao_factory
from owl_core.daos.tag_dao import TagDAO
from owl_core.daos.title_dao import TitleDAO
from owl_core.models.titles import Title
from owl_core.models.users import User
from owl_core.schemas.titles import TitleGet, TitlePost

titles_router = APIRouter(prefix="/titles", tags=["Titles"])

TitleDAODep = Annotated[TitleDAO, Depends(get_dao_factory(TitleDAO))]
TagDAODep = Annotated[TagDAO, Depends(get_dao_factory(TagDAO))]

NotFoundError = HTTPException(status_code=404, detail="Title not found")
ForbiddenError = HTTPException(
    status_code=403, detail="You can only edit or delete your own titles"
)


@titles_router.get("/", response_model=list[TitleGet])
async def get_titles(title_dao: TitleDAODep) -> list[Title]:
    return await title_dao.find_all()


@titles_router.get("/{title_id}", response_model=TitleGet)
async def get_title(title_id: int, title_dao: TitleDAODep) -> Title:
    title_obj: Title | None = await title_dao.find_by_id(title_id)
    if title_obj is None:
        raise NotFoundError
    return title_obj


@titles_router.post("/add", response_model=TitleGet)
async def create_title(
    title: TitlePost,
    current_user: Annotated[User, Depends(get_current_active_user)],
    title_dao: TitleDAODep,
    tag_dao: TagDAODep,
) -> Title:
    command = CreateTitleCommand(title, current_user, title_dao, tag_dao)
    return await command.run()


@titles_router.put("/{title_id}", response_model=TitleGet)
async def update_title(
    title_id: int,
    title: TitlePost,
    current_user: Annotated[User, Depends(get_current_active_user)],
    title_dao: TitleDAODep,
    tag_dao: TagDAODep,
) -> Title:
    title_object: Title | None = await title_dao.find_by_id(title_id)

    if title_object is None:
        raise NotFoundError

    if title_object.author != current_user:
        raise ForbiddenError

    command = UpdateTitleCommand(title_object, title, current_user, title_dao, tag_dao)
    updated_title = await command.run()
    return updated_title


@titles_router.delete("/{title_id}", response_model=TitleGet)
async def delete_title(
    title_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    title_dao: TitleDAODep,
) -> Title:
    title_object: Title | None = await title_dao.find_by_id(title_id)

    if title_object is None:
        raise NotFoundError

    if title_object.author != current_user:
        raise ForbiddenError

    if title_object.reviews:
        raise HTTPException(
            status_code=422, detail="You can not delete titles that have active reviews"
        )
    return await title_dao.delete(title_object)

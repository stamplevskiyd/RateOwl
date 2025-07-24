from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from owl_core.api.users.dependencies import get_current_user
from owl_core.commands.titles.create_title import CreateTitleCommand
from owl_core.commands.titles.update_title import UpdateTitleCommand
from owl_core.daos.dependencies import get_dao_factory
from owl_core.daos.tag_dao import TagDAO
from owl_core.daos.title_dao import TitleDAO
from owl_core.exceptions import NotFoundException, ForbiddenException
from owl_core.models.titles import Title
from owl_core.models.users import User
from owl_core.schemas.titles import TitleGet, TitlePost

titles_router = APIRouter(prefix="/titles", tags=["Titles"])

TitleDAODep = Annotated[TitleDAO, Depends(get_dao_factory(TitleDAO))]
TagDAODep = Annotated[TagDAO, Depends(get_dao_factory(TagDAO))]


@titles_router.get("/")
async def get_titles(title_dao: TitleDAODep) -> list[TitleGet]:
    titles = await title_dao.find_all()
    return [TitleGet.model_validate(title, from_attributes=True) for title in titles]


@titles_router.get("/{title_id}")
async def get_title(title_id: int, title_dao: TitleDAODep) -> TitleGet:
    title_obj: Title | None = await title_dao.find_by_id(title_id)
    if title_obj is None:
        raise NotFoundException(Title)
    return TitleGet.model_validate(title_obj, from_attributes=True)


@titles_router.post(
    "/add", response_model=TitleGet, dependencies=[Depends(get_current_user)]
)  # User is required as an author
async def create_title(
    title: TitlePost,
    title_dao: TitleDAODep,
    tag_dao: TagDAODep,
) -> Title:
    command = CreateTitleCommand(title, title_dao, tag_dao)
    return await command.run()


@titles_router.put("/{title_id}", response_model=TitleGet)
async def update_title(
    title_id: int,
    title: TitlePost,
    current_user: Annotated[User, Depends(get_current_user)],
    title_dao: TitleDAODep,
    tag_dao: TagDAODep,
) -> TitleGet:
    title_object: Title | None = await title_dao.find_by_id(title_id)

    if title_object is None:
        raise NotFoundException(Title)

    if title_object.created_by != current_user:
        raise ForbiddenException

    command = UpdateTitleCommand(title_object, title, title_dao, tag_dao)
    updated_title = await command.run()
    return TitleGet.model_validate(updated_title, from_attributes=True)


@titles_router.delete("/{title_id}", response_model=TitleGet)
async def delete_title(
    title_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    title_dao: TitleDAODep,
) -> Title:
    title_object: Title | None = await title_dao.find_by_id(title_id)

    if title_object is None:
        raise NotFoundException(Title)

    if title_object.created_by != current_user:
        raise ForbiddenException

    if title_object.reviews:
        raise HTTPException(
            status_code=422, detail="You can not delete titles that have active reviews"
        )
    return await title_dao.delete(title_object)

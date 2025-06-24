from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from owl_core.daos.dependencies import get_dao_factory
from owl_core.daos.title_dao import TitleDAO
from owl_core.models.titles import Title
from owl_core.schemas.titles import TitleGet, TitlePost

titles_router = APIRouter(prefix="/titles", tags=["Titles"])

TitleDAODep = Annotated[TitleDAO, Depends(get_dao_factory(TitleDAO))]


@titles_router.get("/", response_model=list[TitleGet])
async def get_titles(title_dao: TitleDAODep) -> list[Title]:
    return await title_dao.find_all()


@titles_router.get("/{title}", response_model=TitleGet)
async def get_title_by_id(title: str, title_dao: TitleDAODep) -> Title:
    title_obj: Title | None = await title_dao.find_one_filtered(Title.slug == title)
    if title_obj is None:
        raise HTTPException(status_code=404, detail="Title not found")
    return title_obj


@titles_router.post("/add", response_model=TitleGet)
async def create_title(title: TitlePost, title_dao: TitleDAODep) -> Title:
    title_dict = title.model_dump()
    return await title_dao.create(title_dict)

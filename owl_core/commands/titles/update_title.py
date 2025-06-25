from fastapi import HTTPException
from owl_core.commands.base_command import BaseCommand
from owl_core.daos.title_dao import TitleDAO
from owl_core.models.titles import Title
from owl_core.models.users import User
from owl_core.schemas.titles import TitlePost

from owl_core.daos.tag_dao import TagDAO
from owl_core.models.tags import Tag


class UpdateTitleCommand(BaseCommand):
    def __init__(
        self,
        title_object: Title,
        title: TitlePost,
        author: User,
        title_dao: TitleDAO,
        tag_dao: TagDAO,
    ):
        self._title = title
        self._title_object = title_object
        self._author = author
        self._title_dao = title_dao
        self._tag_dao = tag_dao
        self._tags: list[Tag] = []

    async def validate(self) -> None:
        tags: list[Tag] = await self._tag_dao.find_by_ids(self._title.tags)
        if len(tags) != len(self._title.tags):
            raise HTTPException(status_code=404, detail="Some of tags not found")
        self._tags = tags

    async def run(self) -> Title:
        await self.validate()
        updated_title = await self._title_dao.update(
            self._title_object, self._title.model_dump() | {"tags": self._tags}
        )
        return updated_title

from owl_core.commands.base_command import BaseCommand
from owl_core.daos.tag_dao import TagDAO
from owl_core.models.tags import Tag
from owl_core.schemas.tags import TagPost


class CreateTagCommand(BaseCommand):
    def __init__(self, tag: TagPost, tag_dao: TagDAO):
        self._tag = tag
        self._tag_dao = tag_dao

    async def validate(self) -> None:
        pass

    async def run(self) -> Tag:
        await self.validate()
        created_tag = await self._tag_dao.create(self._tag.model_dump())
        return created_tag

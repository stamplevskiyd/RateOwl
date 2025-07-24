from owl_core.commands.base_command import BaseCommand
from owl_core.daos.tag_dao import TagDAO
from owl_core.models.tags import Tag
from owl_core.schemas.tags import TagPost


class UpdateTagCommand(BaseCommand):
    def __init__(
        self,
        tag_object: Tag,
        tag: TagPost,
        tag_dao: TagDAO,
    ):
        self._tag = tag
        self._tag_object = tag_object
        self._tag_dao = tag_dao

    async def validate(self) -> None:
        pass

    async def run(self) -> Tag:
        await self.validate()
        updated_tag = await self._tag_dao.update(
            self._tag_object, self._tag.model_dump()
        )
        return updated_tag

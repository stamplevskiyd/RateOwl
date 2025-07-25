from fastapi import HTTPException

from owl_core.commands.base_command import BaseCommand
from owl_core.daos.review_dao import ReviewDAO
from owl_core.daos.title_dao import TitleDAO
from owl_core.models.reviews import Review
from owl_core.models.titles import Title
from owl_core.schemas.reviews import ReviewPost


class CreateReviewCommand(BaseCommand):
    def __init__(
        self,
        review: ReviewPost,
        title_dao: TitleDAO,
        review_dao: ReviewDAO,
    ):
        self._review = review
        self._title_dao = title_dao
        self._review_dao = review_dao

    async def validate(self) -> None:
        title: Title | None = await self._title_dao.find_by_id(self._review.title_id)
        if title is None:
            raise HTTPException(status_code=404, detail="Title not found")

    async def run(self) -> Review:
        await self.validate()
        created_review = await self._review_dao.create(self._review.model_dump())
        return created_review

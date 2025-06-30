from owl_core.commands.base_command import BaseCommand
from owl_core.daos.review_dao import ReviewDAO
from owl_core.models.reviews import Review
from owl_core.schemas.reviews import ReviewPut


class UpdateReviewCommand(BaseCommand):
    def __init__(
        self,
        review_object: Review,
        review: ReviewPut,
        review_dao: ReviewDAO,
    ):
        self._review = review
        self._review_object = review_object
        self._review_dao = review_dao

    async def validate(self) -> None:
        pass

    async def run(self) -> Review:
        await self.validate()
        updated_review = await self._review_dao.update(
            self._review_object, self._review.model_dump()
        )
        return updated_review

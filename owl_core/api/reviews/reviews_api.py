from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException

from owl_core.api.users.dependencies import get_current_active_user
from owl_core.commands.reviews.create_review import CreateReviewCommand
from owl_core.commands.reviews.update_review import UpdateReviewCommand
from owl_core.daos.dependencies import get_dao_factory
from owl_core.daos.review_dao import ReviewDAO
from owl_core.daos.title_dao import TitleDAO
from owl_core.models.reviews import Review
from owl_core.models.users import User
from owl_core.schemas.reviews import ReviewPost, ReviewGet, ReviewPut

reviews_router = APIRouter(prefix="/reviews", tags=["Rates"])


ReviewDAODep = Annotated[ReviewDAO, Depends(get_dao_factory(ReviewDAO))]
TitleDAODep = Annotated[TitleDAO, Depends(get_dao_factory(TitleDAO))]

@reviews_router.get("/")
async def get_reviews(review_dao: ReviewDAODep) -> list[ReviewGet]:
    """Get all available reviews"""
    # TODO: hidden reviews
    reviews = await review_dao.find_all()

    # Review model requires join and pydantic don't seem to support it
    return [ReviewGet.model_validate(r, from_attributes=True) for r in reviews]


@reviews_router.get("/{review_id}")
async def get_review(review_id: int, review_dao: ReviewDAODep) -> ReviewGet:
    """Get a single review"""
    review = await review_dao.find_by_id(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return ReviewGet.model_validate(review, from_attributes=True)


@reviews_router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_review(
    review: ReviewPost,
    current_user: Annotated[User, Depends(get_current_active_user)],
    review_dao: ReviewDAODep,
    title_dao: TitleDAODep,
) -> ReviewGet:
    """Create review"""
    # DAOs use the same session due to the way fastapi handles deps
    command = CreateReviewCommand(review, current_user, title_dao, review_dao)
    created_review = await command.run()
    # Default FastApi pydantic validation does now work with nested models
    return ReviewGet.model_validate(created_review, from_attributes=True)

@reviews_router.put("/{review_id}/update")
async def edit_review(
    review_id: int,
    review: ReviewPut,
    current_user: Annotated[User, Depends(get_current_active_user)],
    review_dao: ReviewDAODep,
    title_dao: TitleDAODep,
) -> ReviewGet:
    """Update review"""
    review_object: Review | None = await review_dao.find_by_id(review_id)

    if review_object is None:
        raise HTTPException(status_code=404, detail="Review not found")

    if review_object.author != current_user:
        raise HTTPException(
            status_code=403, detail="You can only edit your own reviews"
        )

    command = UpdateReviewCommand(review_object, review, title_dao, review_dao)
    updated_review = await command.run()
    return ReviewGet.model_validate(updated_review, from_attributes=True)

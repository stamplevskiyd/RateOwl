from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import or_, BinaryExpression

from owl_core.api.users.dependencies import get_active_user, get_active_user_or_none
from owl_core.commands.reviews.create_review import CreateReviewCommand
from owl_core.commands.reviews.update_review import UpdateReviewCommand
from owl_core.daos.dependencies import get_dao_factory
from owl_core.daos.review_dao import ReviewDAO
from owl_core.daos.title_dao import TitleDAO
from owl_core.models.reviews import Review
from owl_core.models.users import User
from owl_core.schemas.reviews import ReviewPost, ReviewGet, ReviewPut

reviews_router = APIRouter(prefix="/reviews", tags=["Reviews"])


ReviewDAODep = Annotated[ReviewDAO, Depends(get_dao_factory(ReviewDAO))]
TitleDAODep = Annotated[TitleDAO, Depends(get_dao_factory(TitleDAO))]
CurrentUserDep = Annotated[User, Depends(get_active_user)]
UserOrNoneDep = Annotated[User | None, Depends(get_active_user_or_none)]

NotFoundError = HTTPException(status_code=404, detail="Review not found")
ForbiddenError = HTTPException(
    status_code=403, detail="You can only edit or delete your own reviews"
)


# TODO: Move hiding review somewhere else to make it more robust to misses
def get_review_filter(current_user: User) -> BinaryExpression:
    return or_(
        Review.author == None,  # noqa: E711
        Review.hidden == False,  # noqa: E712
        Review.author == current_user,
    )


@reviews_router.get("/")
async def get_reviews(
    review_dao: ReviewDAODep, current_user: UserOrNoneDep
) -> list[ReviewGet]:
    """Get all available reviews"""
    reviews = await review_dao.find_all_filtered(get_review_filter(current_user))

    # Review model requires join and pydantic don't seem to support it
    return [ReviewGet.model_validate(r, from_attributes=True) for r in reviews]


@reviews_router.get("/{review_id}")
async def get_review(
    review_id: int, review_dao: ReviewDAODep, current_user: UserOrNoneDep
) -> ReviewGet:
    """Get a single review"""
    review = await review_dao.find_by_id_filtered(
        review_id, get_review_filter(current_user)
    )
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return ReviewGet.model_validate(review, from_attributes=True)


@reviews_router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_review(
    review: ReviewPost,
    current_user: CurrentUserDep,
    review_dao: ReviewDAODep,
    title_dao: TitleDAODep,
) -> ReviewGet:
    """Create review"""
    # DAOs use the same session due to the way fastapi handles deps
    command = CreateReviewCommand(review, current_user, title_dao, review_dao)
    created_review = await command.run()
    # Default FastApi pydantic validation does now work with nested models
    return ReviewGet.model_validate(created_review, from_attributes=True)


@reviews_router.put("/{review_id}")
async def edit_review(
    review_id: int,
    review: ReviewPut,
    current_user: CurrentUserDep,
    review_dao: ReviewDAODep,
) -> ReviewGet:
    """Update review"""
    review_object: Review | None = await review_dao.find_by_id_filtered(
        review_id, get_review_filter(current_user)
    )

    if review_object is None:
        raise NotFoundError

    if review_object.author != current_user:
        raise ForbiddenError

    command = UpdateReviewCommand(review_object, review, review_dao)
    updated_review = await command.run()
    return ReviewGet.model_validate(updated_review, from_attributes=True)


@reviews_router.delete("/{review_id}")
async def delete_review(
    review_id: int,
    current_user: CurrentUserDep,
    review_dao: ReviewDAODep,
) -> ReviewGet:
    """Update review"""
    review_object: Review | None = await review_dao.find_by_id_filtered(
        review_id, get_review_filter(current_user)
    )

    if review_object is None:
        raise NotFoundError

    if review_object.author != current_user:
        raise ForbiddenError

    deleted_review = await review_dao.delete(review_object)
    return ReviewGet.model_validate(deleted_review, from_attributes=True)

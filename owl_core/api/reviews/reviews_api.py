from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from owl_core.api.users.dependencies import get_current_active_user
from owl_core.daos.dependencies import get_dao_factory
from owl_core.daos.review_dao import ReviewDAO
from owl_core.daos.title_dao import TitleDAO
from owl_core.db.session import get_session
from owl_core.models.reviews import Review
from owl_core.models.titles import Title
from owl_core.models.users import User
from owl_core.schemas.reviews import ReviewPost, ReviewGet

reviews_router = APIRouter(prefix="/reviews", tags=["Rates"])


ReviewDAODep = Annotated[ReviewDAO, Depends(get_dao_factory(ReviewDAO))]


@reviews_router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_review(
    review: ReviewPost,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> ReviewGet:
    # Actually, DAOS will use the same session as fastapi docs say
    # TODO: move to commands
    review_dao = ReviewDAO(session)
    title_dao = TitleDAO(session)

    title: Title | None = await title_dao.find_by_id(review.title_id)
    if title is None:
        raise HTTPException(status_code=404, detail="Title not found")

    created_review = await review_dao.create(
        review.model_dump() | {"author_id": current_user.id}
    )
    # Default FastApi pydantic validation does now work with nested models
    return ReviewGet.model_validate(created_review, from_attributes=True)


@reviews_router.get("/", response_model=ReviewGet)
async def get_reviews(review_dao: ReviewDAODep) -> list[Review]:
    reviews = await review_dao.find_all()
    return reviews


@reviews_router.get("/{review_id}")
async def get_review(review_id: int, review_dao: ReviewDAODep) -> ReviewGet:
    review = await review_dao.find_by_id(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return ReviewGet.model_validate(review, from_attributes=True)

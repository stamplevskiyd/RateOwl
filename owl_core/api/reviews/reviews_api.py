from typing import Annotated, Iterable
from sqlalchemy import select

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from owl_core.db.session import get_session
from owl_core.models.reviews import Review
from owl_core.schemas.reviews import ReviewPost, ReviewGet

reviews_router = APIRouter(prefix="/reviews", tags=["Rates"])


@reviews_router.post(
    "/add", status_code=status.HTTP_201_CREATED, response_model=ReviewGet
)
async def add_review(
    review: ReviewPost, session: Annotated[AsyncSession, Depends(get_session)]
) -> Review:
    new_review = Review(**review.model_dump())
    session.add(new_review)
    await session.commit()
    await session.refresh(new_review)
    return new_review


@reviews_router.get("/", response_model=list[ReviewGet])
async def get_reviews(session: Annotated[AsyncSession, Depends(get_session)]) -> Iterable[Review]:
    query = select(Review)
    reviews = await session.execute(query)
    return reviews.scalars().all()


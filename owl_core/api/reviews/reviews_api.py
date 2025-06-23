from typing import Iterable, Annotated

from fastapi import APIRouter, status, Depends

from owl_core.daos.review_dao import ReviewDAO, get_review_dao
from owl_core.models.reviews import Review
from owl_core.schemas.reviews import ReviewPost, ReviewGet

reviews_router = APIRouter(prefix="/reviews", tags=["Rates"])

ReviewDAODep = Annotated[ReviewDAO, Depends(get_review_dao)]


@reviews_router.post(
    "/add", status_code=status.HTTP_201_CREATED, response_model=ReviewGet
)
async def add_review(review: ReviewPost, review_dao: ReviewDAODep) -> Review:
    return await review_dao.create(review.model_dump())


@reviews_router.get("/", response_model=list[ReviewGet])
async def get_reviews(review_dao: ReviewDAODep) -> Iterable[Review]:
    return await review_dao.find_all()

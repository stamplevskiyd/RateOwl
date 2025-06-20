from fastapi import APIRouter
from owl_core.api.reviews.reviews_api import reviews_router

api_router = APIRouter(prefix="/v1", tags=["v1"])

api_router.include_router(reviews_router)

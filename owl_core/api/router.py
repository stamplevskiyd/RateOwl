from fastapi import APIRouter
from owl_core.api.reviews.reviews_api import reviews_router
from owl_core.api.users.users_api import users_router

api_router = APIRouter(prefix="/v1", tags=["v1"])

api_router.include_router(reviews_router)
api_router.include_router(users_router)

from fastapi import APIRouter
from owl_core.api.reviews.reviews_api import reviews_router
from owl_core.api.users.users_api import users_router
from owl_core.api.titles.titles_api import titles_router
from owl_core.api.tags.tags_api import tags_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(reviews_router)
api_router.include_router(users_router)
api_router.include_router(titles_router)
api_router.include_router(tags_router)

from fastapi import APIRouter
from owl_core.views.users.users_views import users_router

views_router = APIRouter()
views_router.include_router(users_router)

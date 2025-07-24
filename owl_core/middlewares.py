from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from owl_core.context import current_username, current_user_id
from owl_core.users.utils import get_username


class SetUserMiddleware(BaseHTTPMiddleware):
    """Sets current user in ContextVar"""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        token = request.headers.get("Authorization")
        if token:
            username = await get_username(token)
            current_username.set(username)
        # User can be loaded later by dao
        # Not necessary at all
        current_user_id.set(None)
        response = await call_next(request)
        return response

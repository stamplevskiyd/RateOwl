from contextvars import ContextVar

current_username = ContextVar[str | None]("current_username", default=None)
current_user_id = ContextVar[int | None]("current_user_id", default=None)

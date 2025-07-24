from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from owl_core.config import Settings
from owl_core.db.session import get_session
from owl_core.main import app


@pytest_asyncio.fixture()
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Start a test database session."""
    test_settings = Settings()  # type: ignore

    # TODO: Move to test config?
    test_settings.DB_NAME = "test"
    test_settings.DB_USER = "owl"
    test_settings.DB_PASSWORD = "hoot"

    engine = create_async_engine(test_settings.get_db_url())
    session = async_sessionmaker(engine, expire_on_commit=False)()
    yield session
    await session.close()


@pytest.fixture()
def test_app(db_session: AsyncSession) -> FastAPI:
    """Create a test app with overridden dependencies."""
    app.dependency_overrides[get_session] = lambda: db_session
    return app


@pytest_asyncio.fixture()
async def client(test_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """Create an http client."""
    async with AsyncClient(
        transport=ASGITransport(app=test_app), base_url="http://test"
    ) as client:
        yield client

    app.dependency_overrides.clear()

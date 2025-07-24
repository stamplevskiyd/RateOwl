from typing import Annotated

from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from owl_core.config import settings

engine = create_async_engine(settings.get_db_url())

new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_session() as session:
        try:
            yield session
        except SQLAlchemyError:
            await session.rollback()
            raise


SessionDep = Annotated[AsyncSession, Depends(get_session)]

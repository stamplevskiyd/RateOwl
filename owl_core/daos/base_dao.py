from typing import TypeVar, get_args, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from owl_core.db.base import Base

T = TypeVar("T", bound=Base)


class BaseDAO[T]:
    """Base Data Access Object for CRUD operations."""

    """Model class for the DAO."""
    model_cls: type[T] | None = None

    def __init_subclass__(cls) -> None:
        cls.model_cls = get_args(
            cls.__orig_bases__[0]  # type: ignore
        )[0]
        assert cls.model_cls is not None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: dict[str, Any], commit: bool = True) -> T:
        new_obj = self.model_cls(**data)
        self.session.add(new_obj)
        if commit:
            await self.session.commit()
        await self.session.refresh(new_obj)
        return new_obj

    async def find_by_id(self, pk: int) -> T | None:
        """Find an object by its id"""
        # TODO: move to get by pk?
        query = select(self.model_cls).where(self.model_cls.id == pk)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def find_all(self) -> list[T]:
        query = select(self.model_cls)
        result = await self.session.execute(query)
        return result.scalars().all()

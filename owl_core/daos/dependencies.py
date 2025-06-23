from typing import TypeVar, Callable

from sqlalchemy.ext.asyncio import AsyncSession

from owl_core.daos.base_dao import BaseDAO
from owl_core.db.session import SessionDep

T = TypeVar("T", bound=BaseDAO)


def get_dao_factory(dao_class: type[T]) -> Callable[[AsyncSession], T]:
    def get_dao(session: SessionDep) -> T:
        return dao_class(session)

    return get_dao

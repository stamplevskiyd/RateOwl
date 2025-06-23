from sqlalchemy import select, or_

from owl_core.daos.base_dao import BaseDAO
from owl_core.models.users import User


class UserDAO(BaseDAO[User]):
    async def find_by_username_or_email(self, pk: str) -> User | None:
        query = select(User).where(or_(User.username == pk, User.email == pk))
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

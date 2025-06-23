from owl_core.daos.base_dao import BaseDAO
from owl_core.db.session import SessionDep
from owl_core.models.reviews import Review


class ReviewDAO(BaseDAO[Review]):
    """DAO for Review model"""

    pass


async def get_review_dao(session: SessionDep) -> ReviewDAO:
    return ReviewDAO(session)

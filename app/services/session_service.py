from app.services.base_service import BaseService
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.session import Session


class SessionService(BaseService):
    model = Session

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

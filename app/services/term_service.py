from typing import Sequence, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.term import Term
from app.schemas.term import TermCreate, TermUpdate
from app.core.errors import DuplicateEmail
from app.services.base_service import BaseService


class TermService(BaseService):
    model = Term

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    async def create(self, payload: TermCreate) -> Term:
        if await self.exists_by("term", payload.term):
            raise DuplicateEmail("Term already exists")
        return await super().create(payload.dict(exclude_unset=True))

    async def update_by_global_id(self, global_id: str, payload: TermUpdate) -> Term:
        obj = await self.get_by_global_id(global_id)
        if payload.term and payload.term != obj.term:
            existing = await self.get_one_by("term", payload.term)
            if existing:
                raise DuplicateEmail("Term already exists")
        return await super().update_by_global_id(global_id, payload)

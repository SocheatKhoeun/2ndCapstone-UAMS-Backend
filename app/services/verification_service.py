from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.services.base_service import BaseService
from app.models.verification import Verification
from app.schemas.verification import VerificationCreate, VerificationUpdate


class VerificationService(BaseService):
    model = Verification

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    async def create(self, payload: VerificationCreate) -> Verification:
        data = payload.dict(exclude_unset=True)
        session_id = data.get("session_id")
        student_id = data.get("student_id")
        # enforce one active verification per session+student: update existing
        if session_id and student_id:
            q = select(self.model).where((self.model.session_id == session_id) & (self.model.student_id == student_id) & (self.model.active == 1)).limit(1)
            existing = await self.db.scalar(q)
            if existing:
                return await super().update_by_global_id(existing.global_id, VerificationUpdate(**data))

        return await super().create(data)

    async def update_by_global_id(self, global_id: str, payload: VerificationUpdate) -> Verification:
        return await super().update_by_global_id(global_id, payload)

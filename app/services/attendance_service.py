from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.services.base_service import BaseService
from app.models.attendance import Attendance
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate


class AttendanceService(BaseService):
    model = Attendance

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    async def create(self, payload: AttendanceCreate) -> Attendance:
        data = payload.dict(exclude_unset=True)
        # require client to pass exact enum values ('face', 'qr', 'manual')
        session_id = data.get("session_id")
        student_id = data.get("student_id")
        if session_id and student_id:
            q = select(self.model).where((self.model.session_id == session_id) & (self.model.student_id == student_id) & (self.model.active == 1)).limit(1)
            existing = await self.db.scalar(q)
            if existing:
                return await super().update_by_global_id(existing.global_id, AttendanceUpdate(**data))

        return await super().create(data)

    async def update_by_global_id(self, global_id: str, payload: AttendanceUpdate) -> Attendance:
        if hasattr(payload, "dict"):
            data = payload.dict(exclude_unset=True)
        else:
            data = dict(payload or {})
        # do not alter 'method' value; require exact enum strings
        return await super().update_by_global_id(global_id, data)

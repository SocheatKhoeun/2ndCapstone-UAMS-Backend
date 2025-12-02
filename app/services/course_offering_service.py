from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.base_service import BaseService
from app.models.course_offering import CourseOffering
from app.schemas.course_offering import CourseOfferingCreate, CourseOfferingUpdate
from app.core.errors import DuplicateEmail


class CourseOfferingService(BaseService):
    model = CourseOffering

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    async def create(self, payload: CourseOfferingCreate) -> CourseOffering:
        # Map legacy `room` field to `room_id` if present
        data = payload.dict(exclude_unset=True)
        if "room" in data and "room_id" not in data:
            data["room_id"] = data.pop("room")
        # Accept integer timestamps (milliseconds since epoch) for start_time/end_time
        for t in ("start_time", "end_time"):
            if t in data and isinstance(data[t], (int, float)):
                # BaseService._ms_to_dt expects milliseconds
                try:
                    data[t] = self._ms_to_dt(int(data[t]))
                except Exception:
                    # leave as-is; validation will catch incorrect types
                    pass
        return await super().create(data)

    async def update_by_global_id(self, global_id: str, payload: CourseOfferingUpdate) -> CourseOffering:
        data = payload.dict(exclude_unset=True)
        if "room" in data and "room_id" not in data:
            data["room_id"] = data.pop("room")
        # Accept integer timestamps (milliseconds since epoch) for start_time/end_time
        for t in ("start_time", "end_time"):
            if t in data and isinstance(data[t], (int, float)):
                try:
                    data[t] = self._ms_to_dt(int(data[t]))
                except Exception:
                    pass
        return await super().update_by_global_id(global_id, data)

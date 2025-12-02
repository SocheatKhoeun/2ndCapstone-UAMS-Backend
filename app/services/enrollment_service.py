from app.services.base_service import BaseService
from app.models.enrollment import Enrollment
from sqlalchemy import select
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError


class EnrollmentService(BaseService):
    model = Enrollment
    # Enrollments use the `active` column to represent active/inactive/deleted states.
    # Do not override BaseService.status_column which defaults to 'active'.

    async def create(self, payload):
        # normalize payload to dict (BaseService.create supports Pydantic too,
        # but we want to check duplicates first)
        if hasattr(payload, "dict"):
            data = payload.dict(exclude_unset=True, exclude_none=True)
        else:
            data = dict(payload or {})

        student_id = data.get("student_id")
        offering_id = data.get("offering_id")
        if student_id is None or offering_id is None:
            raise HTTPException(status_code=400, detail="student_id and offering_id are required")

        # check existing enrollment
        q = select(Enrollment).where(Enrollment.student_id == student_id, Enrollment.offering_id == offering_id)
        exists = await self.db.scalar(q)
        if exists:
            raise HTTPException(status_code=400, detail="Student already enrolled in this offering")

        # fallback to BaseService.create but catch DB IntegrityError defensively
        try:
            return await super().create(data)
        except IntegrityError as e:
            # if unique constraint still violated, return client-friendly error
            raise HTTPException(status_code=400, detail="Student already enrolled in this offering")

    async def update_by_global_id(self, global_id: str, payload):
        # normalize payload to dict
        if hasattr(payload, "dict"):
            data = payload.dict(exclude_unset=True, exclude_none=True)
        else:
            data = dict(payload or {})

        # fetch current row (uses BaseService.get_by_global_id to enforce access rules)
        current = await self.get_by_global_id(global_id)

        new_student = data.get("student_id", getattr(current, "student_id"))
        new_offering = data.get("offering_id", getattr(current, "offering_id"))

        # if student/offering pair changes, ensure no other row has the same pair
        q = select(Enrollment).where(Enrollment.student_id == new_student, Enrollment.offering_id == new_offering, Enrollment.id != getattr(current, "id"))
        exists = await self.db.scalar(q)
        if exists:
            raise HTTPException(status_code=400, detail="Another enrollment with this student and offering already exists")

        try:
            return await super().update_by_global_id(global_id, data)
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Another enrollment with this student and offering already exists")

    async def set_active_by_global_id(self, global_id: str, value: int):
        """Explicitly set the `active` column on an enrollment by global_id.

        This is used by the admin route that previously updated `status`.
        Value should be 0 (inactive) or 1 (active). Deleted state (2) can also be used.
        """
        # delegate to BaseService.set_status_by_global_id which uses self.status_column
        return await self.set_status_by_global_id(global_id, value)

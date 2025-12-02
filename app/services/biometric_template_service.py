from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.services.base_service import BaseService
from app.models.biometric_template import BiometricTemplate
from app.schemas.biometric_template import BiometricTemplateCreate, BiometricTemplateUpdate
from app.core.errors import DuplicateEmail


class BiometricTemplateService(BaseService):
    model = BiometricTemplate

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    async def create(self, payload: BiometricTemplateCreate) -> BiometricTemplate:
        # Enforce one biometric template per student: if payload contains student_id,
        # attempt to find an existing active template for that student and replace it.
        data = payload.dict(exclude_unset=True)
        student_id = data.get("student_id")
        if student_id:
            # try to find existing active template for this student
            q = select(self.model).where((self.model.student_id == student_id) & (self.model.active == 1)).limit(1)
            existing = await self.db.scalar(q)
            if existing:
                # update the existing template by its global_id
                return await super().update_by_global_id(existing.global_id, BiometricTemplateUpdate(**data))

        # fallback: create new template
        return await super().create(data)

    async def update_by_global_id(self, global_id: str, payload: BiometricTemplateUpdate) -> BiometricTemplate:
        return await super().update_by_global_id(global_id, payload)

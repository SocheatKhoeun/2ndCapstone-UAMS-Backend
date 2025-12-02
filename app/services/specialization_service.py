from typing import Sequence, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.specialization import Specialization
from app.schemas.specialization import SpecializationCreate, SpecializationUpdate
from app.core.errors import DuplicateEmail, NotFound
from app.core.errors import InvalidPasswordLength
from app.services.base_service import BaseService

class SpecializationService(BaseService):
    """Business logic for Specializations. No FastAPI imports here."""
    model = Specialization

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    async def create(self, payload: SpecializationCreate) -> Specialization:
        if await self.exists_by("name", payload.name):
            raise DuplicateEmail("Specialization name already registered")
        Specialization = await super().create(payload.dict(exclude_unset=True))
        return Specialization

    async def update_by_global_id(self, global_id: str, payload: SpecializationUpdate) -> Specialization:
        obj = await self.get_by_global_id(global_id)
        # if changing Specialization name, ensure uniqueness
        if payload.name and payload.name != obj.name:
            existing = await self.get_one_by("name", payload.name)
            if existing:
                raise DuplicateEmail("Specialization name already registered")

        # Delegate the actual update logic to BaseService to avoid duplication
        return await super().update_by_global_id(global_id, payload)
    

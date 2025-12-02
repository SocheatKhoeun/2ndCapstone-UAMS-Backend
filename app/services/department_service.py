from typing import Sequence, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.department import Department
from app.schemas.department import DepartmentCreate, DepartmentUpdate
from app.core.errors import DuplicateEmail, NotFound
from app.core.errors import InvalidPasswordLength
from app.services.base_service import BaseService

class DepartmentService(BaseService):
    """Business logic for departments. No FastAPI imports here."""
    model = Department

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    async def create(self, payload: DepartmentCreate) -> Department:
        if await self.exists_by("name", payload.name):
            raise DuplicateEmail("Department name already registered")
        department = await super().create(payload.dict(exclude_unset=True))
        return department

    async def update_by_global_id(self, global_id: str, payload: DepartmentUpdate) -> Department:
        obj = await self.get_by_global_id(global_id)
        # if changing department name, ensure uniqueness
        if payload.name and payload.name != obj.name:
            existing = await self.get_one_by("name", payload.name)
            if existing:
                raise DuplicateEmail("Department name already registered")

        # Delegate the actual update logic to BaseService to avoid duplication
        return await super().update_by_global_id(global_id, payload)
    

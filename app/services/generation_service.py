from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.services.base_service import BaseService
from app.models.generation import Generation
from app.schemas.generation import GenerationCreate, GenerationUpdate
from app.core.errors import DuplicateEmail, NotFound


class GenerationService(BaseService):
    model = Generation

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    async def create(self, payload: GenerationCreate) -> Generation:
        # ensure unique generation name
        existing = await self.get_one_by("generation", payload.generation)
        if existing:
            raise DuplicateEmail("Generation already exists")
        generation = await super().create(payload.dict(exclude_unset=True))
        return generation

    async def update_by_global_id(self, global_id: str, payload: GenerationUpdate) -> Generation:
        obj = await self.get_by_global_id(global_id)
        # if changing generation name, ensure uniqueness
        if payload.generation and payload.generation != obj.generation:
            existing = await self.get_one_by("generation", payload.generation)
            if existing:
                raise DuplicateEmail("Generation already exists")
        for k, v in payload.dict(exclude_unset=True).items():
            setattr(obj, k, v)
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj
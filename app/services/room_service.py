from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.base_service import BaseService
from app.models.room import Room
from app.schemas.room import RoomCreate, RoomUpdate
from app.core.errors import DuplicateEmail


class RoomService(BaseService):
    model = Room

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    async def create(self, payload: RoomCreate) -> Room:
        if await self.exists_by("room", payload.room):
            raise DuplicateEmail("Room with this name already exists")
        return await super().create(payload.dict(exclude_unset=True))

    async def update_by_global_id(self, global_id: str, payload: RoomUpdate) -> Room:
        obj = await self.get_by_global_id(global_id)
        if payload.room and payload.room != obj.room:
            existing = await self.get_one_by("room", payload.room)
            if existing:
                raise DuplicateEmail("Room with this name already exists")
        return await super().update_by_global_id(global_id, payload)

from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.base_service import BaseService
from app.models.group import Group
from app.schemas.group import GroupCreate, GroupUpdate
from app.core.errors import DuplicateEmail


class GroupService(BaseService):
    model = Group

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    async def create(self, payload: GroupCreate) -> Group:
        # uniqueness check for group_name
        if await self.exists_by("group_name", payload.group_name):
            raise DuplicateEmail("Group with this name already exists")
        # delegate creation to BaseService
        return await super().create(payload.dict(exclude_unset=True))

    async def update_by_global_id(self, global_id: str, payload: GroupUpdate) -> Group:
        obj = await self.get_by_global_id(global_id)
        if payload.group_name and payload.group_name != obj.group_name:
            existing = await self.get_one_by("group_name", payload.group_name)
            if existing:
                raise DuplicateEmail("Group with this name already exists")
        return await super().update_by_global_id(global_id, payload)

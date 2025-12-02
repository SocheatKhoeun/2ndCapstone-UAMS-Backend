from typing import Sequence, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.setting import Setting
from app.schemas.setting import SettingCreate, SettingUpdate
from app.core.errors import NotFound
from app.services.base_service import BaseService, generic_list, generic_count

class SettingService(BaseService):
    model = Setting

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    

from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.setting_service import SettingService
from app.schemas.setting import SettingCreate, SettingUpdate, SettingOut
from app.core.errors import NotFound
from app.api.response import success_response
from uuid import uuid4


def get_service(db: AsyncSession = Depends(get_db), request: Request = None)-> SettingService:
    svc = SettingService(db)
    # attach request so BaseService.list may read query params directly
    svc.request = request
    return svc

async def create_setting(payload: SettingCreate, svc: SettingService = Depends(get_service)) -> SettingOut:
    # svc.create expects a mapping; convert Pydantic model to dict
    if await svc.get_one_by("key", payload.key):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Setting with this key already exists")
    # Pydantic schema and DB model provide a default for global_id; just pass the mapping
    setting = await svc.create(payload.__dict__)
    return success_response({"id": setting.id}, message="Setting created", code=201)

async def list_settings(svc: SettingService = Depends(get_service)) -> list[SettingOut]:
    payload = await svc.list()
    return success_response(payload, message="Settings retrieved successfully")

async def get_setting(global_id: str, svc: SettingService = Depends(get_service)) -> SettingOut:
    # Use key (string) as the stable identifier for settings
    setting = await svc.get_by_global_id(global_id)
    return success_response(setting, message="Setting retrieved successfully")

async def update_setting(global_id: str, payload: SettingUpdate, svc: SettingService = Depends(get_service)) -> SettingOut:
    existing = await svc.get_by_global_id(global_id)
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Setting not found")
    # If client provided a new `key`, ensure it's not already used by another setting
    new_key = getattr(payload, "key", None)
    if new_key is not None and new_key != existing.key:
        other = await svc.get_one_by("key", new_key)
        if other:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="that key is already in use")

    setting = await svc.update_by_global_id(global_id, payload)
    return success_response(setting, message="Setting updated successfully", schema=SettingOut)

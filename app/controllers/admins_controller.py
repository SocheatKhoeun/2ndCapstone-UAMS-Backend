import json
from fastapi import Depends, Request, Query
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.admin_service import AdminService
from app.schemas.admin import AdminCreate, AdminUpdate, AdminOut, ActiveUpdate
from app.api.response import success_response
from fastapi import Request

def get_service(db: AsyncSession = Depends(get_db), request: Request = None) -> AdminService:
    svc = AdminService(db)
    # attach request so BaseService.list may read query params directly
    svc.request = request
    return svc

async def create_admin(payload: AdminCreate, svc: AdminService = Depends(get_service)) -> AdminOut:
    admin = await svc.create(payload)
    return success_response(admin, message="Admin created successfully", schema=AdminOut)

async def list_admins(svc: AdminService = Depends(get_service)) -> list[AdminOut]:
    payload = await svc.list()
    return success_response(payload, message="Admins retrieved successfully", schema=AdminOut)

async def get_admin(global_id: str, svc: AdminService = Depends(get_service)) -> AdminOut:
    admin = await svc.get_by_global_id(global_id)
    return success_response(admin, message="Admin retrieved successfully", schema=AdminOut)

async def update_admin(global_id: str, payload: AdminUpdate, svc: AdminService = Depends(get_service)) -> AdminOut:
    admin = await svc.update_by_global_id(global_id, payload)
    return success_response(admin, message="Admin updated successfully", schema=AdminOut)

async def set_active_admin(global_id: str, payload: ActiveUpdate, svc: AdminService = Depends(get_service)) -> AdminOut:
    admin = await svc.set_status_by_global_id(global_id, payload.value)
    return success_response(admin, message="Admin activation status updated successfully", schema=AdminOut)

# async def delete_admin(global_id: str, svc: AdminService = Depends(get_service)) -> None:
#     admin = await svc.set_status_by_global_id(global_id, 2)
#     return success_response(admin, message="Admin deleted successfully", schema=AdminOut)
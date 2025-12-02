import json
from fastapi import Depends, Request, Query
from app.api.deps_helpers import resolve_body_and_fk
from app.models.department import Department
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.specialization_service import SpecializationService
from app.schemas.specialization import SpecializationCreate, SpecializationUpdate, SpecializationOut, ActiveUpdate
from app.api.response import success_response
from fastapi import Request

def get_service(db: AsyncSession = Depends(get_db), request: Request = None) -> SpecializationService:
    svc = SpecializationService(db)
    # attach request so BaseService.list may read query params directly
    svc.request = request
    return svc

async def create_specialization(payload: SpecializationCreate = Depends(resolve_body_and_fk(SpecializationCreate, {"department_id": Department})), svc: SpecializationService = Depends(get_service)) -> SpecializationOut:
    specialization = await svc.create(payload)
    return success_response(specialization, message="Specialization created successfully", schema=SpecializationOut)

async def list_specializations(svc: SpecializationService = Depends(get_service)) -> list[SpecializationOut]:
    payload = await svc.list()
    return success_response(payload, message="Specialization retrieved successfully", schema=SpecializationOut)

async def get_specialization(global_id: str, svc: SpecializationService = Depends(get_service)) -> SpecializationOut:
    specialization = await svc.get_by_global_id(global_id)
    return success_response(specialization, message="Specialization retrieved successfully", schema=SpecializationOut)

async def update_specialization(global_id: str, payload: SpecializationUpdate = Depends(resolve_body_and_fk(SpecializationUpdate, {"department_id": Department})), svc: SpecializationService = Depends(get_service)) -> SpecializationOut:
    specialization = await svc.update_by_global_id(global_id, payload)
    return success_response(specialization, message="Specialization updated successfully", schema=SpecializationOut)

async def set_active_specialization(global_id: str, payload: ActiveUpdate, svc: SpecializationService = Depends(get_service)) -> SpecializationOut:
    specialization = await svc.set_status_by_global_id(global_id, payload.value)
    return success_response(specialization, message="Specialization activation status updated successfully", schema=SpecializationOut)

async def delete_specialization(global_id: str, svc: SpecializationService = Depends(get_service)) -> None:
    specialization = await svc.set_status_by_global_id(global_id, 2)
    return success_response(specialization, message="Specialization deleted successfully", schema=SpecializationOut)
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.biometric_template_service import BiometricTemplateService
from app.schemas.biometric_template import (
    BiometricTemplateCreate,
    BiometricTemplateUpdate,
    BiometricTemplateOut,
    BiometricTemplatesPage,
    ActiveUpdate,
)
from app.api.response import success_response
from app.api.deps_helpers import resolve_body_and_fk
from app.models.student import Student


def get_service(db: AsyncSession = Depends(get_db), request: Request = None) -> BiometricTemplateService:
    svc = BiometricTemplateService(db)
    svc.request = request
    return svc


async def create_biometric_template(payload: BiometricTemplateCreate = Depends(resolve_body_and_fk(BiometricTemplateCreate, {"student_id": Student})), svc: BiometricTemplateService = Depends(get_service)) -> BiometricTemplateOut:
    obj = await svc.create(payload)
    return success_response(obj, message="Biometric template created successfully", schema=BiometricTemplateOut)


async def list_biometric_templates(svc: BiometricTemplateService = Depends(get_service)) -> list[BiometricTemplateOut]:
    objs = await svc.list()
    return success_response(objs, message="Biometric templates retrieved successfully", schema=BiometricTemplateOut)


async def get_biometric_template(global_id: str, svc: BiometricTemplateService = Depends(get_service)) -> BiometricTemplateOut:
    obj = await svc.get_by_global_id(global_id)
    return success_response(obj, message="Biometric template retrieved successfully", schema=BiometricTemplateOut)


async def update_biometric_template(global_id: str, payload: BiometricTemplateUpdate = Depends(resolve_body_and_fk(BiometricTemplateUpdate, {"student_id": Student})), svc: BiometricTemplateService = Depends(get_service)) -> BiometricTemplateOut:
    obj = await svc.update_by_global_id(global_id, payload)
    return success_response(obj, message="Biometric template updated successfully", schema=BiometricTemplateOut)


async def set_active_biometric_template(global_id: str, payload: ActiveUpdate, svc: BiometricTemplateService = Depends(get_service)) -> BiometricTemplateOut:
    # reuse BaseService.set_status_by_global_id for active handling (value int expected)
    obj = await svc.set_status_by_global_id(global_id, payload.value)
    return success_response(obj, message="Biometric template activation status updated successfully", schema=BiometricTemplateOut)


async def delete_biometric_template(global_id: str, svc: BiometricTemplateService = Depends(get_service)) -> None:
    obj = await svc.set_status_by_global_id(global_id, 2)
    return success_response(obj, message="Biometric template deleted successfully", schema=BiometricTemplateOut)

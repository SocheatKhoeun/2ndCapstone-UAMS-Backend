from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.verification_service import VerificationService
from app.schemas.verification import (
    VerificationCreate,
    VerificationUpdate,
    VerificationOut,
    VerificationsPage,
    ActiveUpdate,
)
from app.api.response import success_response
from app.api.deps_helpers import resolve_body_and_fk
from app.models.student import Student
from app.models.session import Session
from app.models.biometric_template import BiometricTemplate


def get_service(db: AsyncSession = Depends(get_db), request: Request = None) -> VerificationService:
    svc = VerificationService(db)
    svc.request = request
    return svc


async def create_verification(payload: VerificationCreate = Depends(resolve_body_and_fk(VerificationCreate, {"student_id": Student, "session_id": Session, "template_id": BiometricTemplate})), svc: VerificationService = Depends(get_service)) -> VerificationOut:
    obj = await svc.create(payload)
    return success_response(obj, message="Verification created successfully", schema=VerificationOut)


async def list_verifications(svc: VerificationService = Depends(get_service)) -> list[VerificationOut]:
    objs = await svc.list()
    return success_response(objs, message="Verifications retrieved successfully", schema=VerificationOut)


async def get_verification(global_id: str, svc: VerificationService = Depends(get_service)) -> VerificationOut:
    obj = await svc.get_by_global_id(global_id)
    return success_response(obj, message="Verification retrieved successfully", schema=VerificationOut)


async def update_verification(global_id: str, payload: VerificationUpdate = Depends(resolve_body_and_fk(VerificationUpdate, {"student_id": Student, "session_id": Session, "template_id": BiometricTemplate})), svc: VerificationService = Depends(get_service)) -> VerificationOut:
    obj = await svc.update_by_global_id(global_id, payload)
    return success_response(obj, message="Verification updated successfully", schema=VerificationOut)

async def set_active_verification(global_id: str, payload: ActiveUpdate, svc: VerificationService = Depends(get_service)) -> VerificationOut:
    # reuse BaseService.set_status_by_global_id for active handling (value int expected)
    obj = await svc.set_status_by_global_id(global_id, payload.value)
    return success_response(obj, message="Verification activation status updated successfully", schema=VerificationOut)

async def delete_verification(global_id: str, svc: VerificationService = Depends(get_service)) -> None:
    obj = await svc.set_status_by_global_id(global_id, 2)
    return success_response(obj, message="Verification deleted successfully", schema=VerificationOut)

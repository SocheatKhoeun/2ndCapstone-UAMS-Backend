from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.admin import ActiveUpdate
from app.services.attendance_service import AttendanceService
from app.schemas.attendance import (
    AttendanceCreate,
    AttendanceUpdate,
    AttendanceOut,
    AttendancesPage,
)
from app.api.response import success_response
from app.api.deps_helpers import resolve_body_and_fk
from app.models.student import Student
from app.models.session import Session
from app.controllers.verification_controller import VerificationService
from app.models.verification import Verification


def get_service(db: AsyncSession = Depends(get_db), request: Request = None) -> AttendanceService:
    svc = AttendanceService(db)
    svc.request = request
    return svc


async def create_attendance(payload: AttendanceCreate = Depends(resolve_body_and_fk(AttendanceCreate, {"student_id": Student, "session_id": Session, "verification_id": Verification})), svc: AttendanceService = Depends(get_service)) -> AttendanceOut:
    obj = await svc.create(payload)
    return success_response(obj, message="Attendance created successfully", schema=AttendanceOut)


async def list_attendances(svc: AttendanceService = Depends(get_service)) -> list[AttendanceOut]:
    objs = await svc.list()
    return success_response(objs, message="Attendances retrieved successfully", schema=AttendanceOut)


async def get_attendance(global_id: str, svc: AttendanceService = Depends(get_service)) -> AttendanceOut:
    obj = await svc.get_by_global_id(global_id)
    return success_response(obj, message="Attendance retrieved successfully", schema=AttendanceOut)


async def update_attendance(global_id: str, payload: AttendanceUpdate = Depends(resolve_body_and_fk(AttendanceUpdate, {"student_id": Student, "session_id": Session, "verification_id": Verification})), svc: AttendanceService = Depends(get_service)) -> AttendanceOut:
    obj = await svc.update_by_global_id(global_id, payload)
    return success_response(obj, message="Attendance updated successfully", schema=AttendanceOut)

async def update_active_status(global_id: str, payload: ActiveUpdate, svc: AttendanceService = Depends(get_service)) -> AttendanceOut:
    # reuse BaseService.set_status_by_global_id for active handling (value int expected)
    obj = await svc.set_status_by_global_id(global_id, payload.value)
    return success_response(obj, message="Attendance active status updated successfully", schema=AttendanceOut)

async def delete_attendance(global_id: str, svc: AttendanceService = Depends(get_service)) -> None:
    obj = await svc.set_status_by_global_id(global_id, 2)
    return success_response(obj, message="Attendance deleted successfully", schema=AttendanceOut)

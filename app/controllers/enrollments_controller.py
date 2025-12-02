from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.enrollment_service import EnrollmentService
from app.schemas.enrollment import (
    EnrollmentCreate,
    EnrollmentUpdate,
    EnrollmentOut,
    EnrollmentsPage,
)
from app.schemas.admin import ActiveUpdate
from app.api.response import success_response
from app.api.deps_helpers import resolve_body_and_fk
from app.models.student import Student
from app.models.course_offering import CourseOffering
from fastapi import HTTPException


def get_service(db: AsyncSession = Depends(get_db), request: Request = None) -> EnrollmentService:
    svc = EnrollmentService(db)
    svc.request = request
    return svc


async def create_enrollment(payload: EnrollmentCreate = Depends(resolve_body_and_fk(EnrollmentCreate, {"student_id": Student, "offering_id": CourseOffering})), svc: EnrollmentService = Depends(get_service)) -> EnrollmentOut:
    obj = await svc.create(payload)
    return success_response(obj, message="Enrollment created successfully", schema=EnrollmentOut)


async def list_enrollments(svc: EnrollmentService = Depends(get_service)) -> list[EnrollmentOut]:
    objs = await svc.list()
    return success_response(objs, message="Enrollments retrieved successfully", schema=EnrollmentOut)


async def get_enrollment(global_id: str, svc: EnrollmentService = Depends(get_service)) -> EnrollmentOut:
    obj = await svc.get_by_global_id(global_id)
    return success_response(obj, message="Enrollment retrieved successfully", schema=EnrollmentOut)


async def update_enrollment(global_id: str, payload: EnrollmentUpdate = Depends(resolve_body_and_fk(EnrollmentUpdate, {"student_id": Student, "offering_id": CourseOffering})), svc: EnrollmentService = Depends(get_service)) -> EnrollmentOut:
    obj = await svc.update_by_global_id(global_id, payload)
    return success_response(obj, message="Enrollment updated successfully", schema=EnrollmentOut)

async def set_active_enrollment(global_id: str, payload: ActiveUpdate, svc: EnrollmentService = Depends(get_service)) -> EnrollmentOut:
    # For enrollments the /status endpoint should toggle the `active` column
    # (not the `status` column). Use a dedicated service method to update it.
    obj = await svc.set_active_by_global_id(global_id, payload.value)
    return success_response(obj, message="Enrollment activation status updated successfully", schema=EnrollmentOut)

async def delete_enrollment(global_id: str, svc: EnrollmentService = Depends(get_service)) -> None:
    obj = await svc.set_status_by_global_id(global_id, 2)
    return success_response(obj, message="Enrollment deleted successfully", schema=EnrollmentOut)

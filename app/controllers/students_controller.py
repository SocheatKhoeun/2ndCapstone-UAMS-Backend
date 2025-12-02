from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.student_service import StudentService
from app.schemas.student import StudentCreate, StudentUpdate, StudentOut, ActiveUpdate
from app.core.errors import NotFound
from app.api.response import success_response
from app.api.response import success_response


def get_service(db: AsyncSession = Depends(get_db), request: Request = None) -> StudentService:
    svc = StudentService(db)
    svc.request = request
    return svc


async def create_student(payload: StudentCreate, svc: StudentService = Depends(get_service)) -> StudentOut:
    student = await svc.create(payload)
    return success_response(student, message="Student created", schema=StudentOut)


async def list_students(svc: StudentService = Depends(get_service)) -> list[StudentOut]:
    payload = await svc.list()
    return success_response(payload, message="Students retrieved successfully", schema=StudentOut)


async def get_student(global_id: str, svc: StudentService = Depends(get_service)) -> StudentOut:
    student = await svc.get_by_global_id(global_id)
    return success_response(student, message="Student retrieved successfully", schema=StudentOut)


async def update_student(global_id: str, payload: StudentUpdate, svc: StudentService = Depends(get_service)) -> StudentOut:
    student = await svc.update_by_global_id(global_id, payload)
    return success_response(student, message="Student updated successfully", schema=StudentOut)

async def set_active_student(global_id: str, payload: ActiveUpdate, svc: StudentService = Depends(get_service)) -> StudentOut:
    student = await svc.set_status_by_global_id(global_id, payload.value)
    return success_response(student, message="Student activation status updated successfully", schema=StudentOut)

async def delete_student(global_id: str, svc: StudentService = Depends(get_service)) -> None:
    student = await svc.delete_by_global_id(global_id)
    return success_response(student, message="Student deleted successfully", schema=StudentOut)

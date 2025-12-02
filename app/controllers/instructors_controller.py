from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.instructor_service import InstructorService
from app.schemas.instructor import InstructorCreate, InstructorUpdate, InstructorOut, ActiveUpdate
from app.core.errors import NotFound
from app.api.response import success_response

def get_service(db: AsyncSession = Depends(get_db), request: Request = None) -> InstructorService:
    svc = InstructorService(db)
    svc.request = request
    return svc

async def create_instructor(payload: InstructorCreate, svc: InstructorService = Depends(get_service)) -> InstructorOut:
    inst = await svc.create(payload)
    return success_response(inst, message="Instructor created", schema=InstructorOut)

async def list_instructors(svc: InstructorService = Depends(get_service)) -> list[InstructorOut]:
    payload = await svc.list()
    return success_response(payload, message="Instructors retrieved successfully", schema=InstructorOut)

async def get_instructor(global_id: str, svc: InstructorService = Depends(get_service)) -> InstructorOut:
    inst = await svc.get_by_global_id(global_id)
    return success_response(inst, message="Instructor retrieved successfully", schema=InstructorOut)

async def update_instructor(global_id: str, payload: InstructorUpdate, svc: InstructorService = Depends(get_service)) -> InstructorOut:
    inst = await svc.update_by_global_id(global_id, payload)
    return success_response(inst, message="Instructor updated successfully", schema=InstructorOut)

async def set_active_instructor(global_id: str, payload: ActiveUpdate, svc: InstructorService = Depends(get_service)) -> InstructorOut:
    inst = await svc.set_status_by_global_id(global_id, payload.value)
    return success_response(inst, message="Instructor status updated successfully", schema=InstructorOut)

# async def delete_instructor(global_id: str, svc: InstructorService = Depends(get_service)) -> None:
#     inst = await svc.delete_by_global_id(global_id)
#     return success_response(inst, message="Instructor deleted successfully", schema=InstructorOut)

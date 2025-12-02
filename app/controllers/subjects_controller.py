import json
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.subject_service import SubjectService
from app.schemas.subject import SubjectCreate, SubjectOut, SubjectsPage, SubjectUpdate, ActiveUpdate
from app.api.response import success_response
from fastapi import Request

def get_service(db: AsyncSession = Depends(get_db), request: Request = None) -> SubjectService:
    svc = SubjectService(db)
    # attach request so BaseService.list may read query params directly
    svc.request = request
    return svc

async def create_subject(payload: SubjectCreate, svc: SubjectService = Depends(get_service)) -> SubjectOut:
    subject = await svc.create(payload)
    return success_response(subject, message="Subject created successfully", schema=SubjectOut)

async def list_subjects(svc: SubjectService = Depends(get_service)) -> list[SubjectOut]:
    subjects = await svc.list()
    return success_response(subjects, message="Subjects retrieved successfully", schema=SubjectOut)

async def get_subject(global_id: str, svc: SubjectService = Depends(get_service)) -> SubjectOut:
    subject = await svc.get_by_global_id(global_id)
    return success_response(subject, message="Subject retrieved successfully", schema=SubjectOut)

async def update_subject(global_id: str, payload: SubjectUpdate, svc: SubjectService = Depends(get_service)) -> SubjectOut:
    subject = await svc.update_by_global_id(global_id, payload)
    return success_response(subject, message="Subject updated successfully", schema=SubjectOut)

async def set_active_subject(global_id: str, payload: ActiveUpdate, svc: SubjectService = Depends(get_service)) -> SubjectOut:
    subject = await svc.set_status_by_global_id(global_id, payload.value)
    return success_response(subject, message="Subject activation status updated successfully", schema=SubjectOut)

async def delete_subject(global_id: str, svc: SubjectService = Depends(get_service)) -> None:
    subject = await svc.set_status_by_global_id(global_id, 2)
    return success_response(subject, message="Subject deleted successfully", schema=SubjectOut)
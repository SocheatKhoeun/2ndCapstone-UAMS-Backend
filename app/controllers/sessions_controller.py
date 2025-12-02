from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.department import ActiveUpdate
from app.services.session_service import SessionService
from app.schemas.session import (
    SessionCreate,
    SessionUpdate,
    SessionOut,
    SessionsPage,
)
from app.api.response import success_response
from app.api.deps_helpers import resolve_body_and_fk
from app.models.course_offering import CourseOffering
from app.models.room import Room


def get_service(db: AsyncSession = Depends(get_db), request: Request = None) -> SessionService:
    svc = SessionService(db)
    svc.request = request
    return svc


async def create_session(payload: SessionCreate = Depends(resolve_body_and_fk(SessionCreate, {"offering_id": CourseOffering, "room_id": Room})), svc: SessionService = Depends(get_service)) -> SessionOut:
    obj = await svc.create(payload)
    return success_response(obj, message="Session created successfully", schema=SessionOut)


async def list_sessions(svc: SessionService = Depends(get_service)) -> list[SessionOut]:
    objs = await svc.list()
    return success_response(objs, message="Sessions retrieved successfully", schema=SessionOut)


async def get_session(global_id: str, svc: SessionService = Depends(get_service)) -> SessionOut:
    obj = await svc.get_by_global_id(global_id)
    return success_response(obj, message="Session retrieved successfully", schema=SessionOut)


async def update_session(global_id: str, payload: SessionUpdate = Depends(resolve_body_and_fk(SessionUpdate, {"offering_id": CourseOffering, "room_id": Room})), svc: SessionService = Depends(get_service)) -> SessionOut:
    obj = await svc.update_by_global_id(global_id, payload)
    return success_response(obj, message="Session updated successfully", schema=SessionOut)

async def update_active_status(global_id: str, payload: ActiveUpdate, svc: SessionService = Depends(get_service)) -> SessionOut:
    obj = await svc.set_status_by_global_id(global_id, payload.value)
    return success_response(obj, message="Session active status updated successfully", schema=SessionOut)

async def delete_session(global_id: str, svc: SessionService = Depends(get_service)) -> None:
    obj = await svc.set_status_by_global_id(global_id, 2)
    return success_response(obj, message="Session deleted successfully", schema=SessionOut)

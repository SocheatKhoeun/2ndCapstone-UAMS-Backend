import json
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.term_service import TermService
from app.schemas.term import TermCreate, TermOut, TermsPage, TermUpdate, ActiveUpdate
from app.api.response import success_response


def get_service(db: AsyncSession = Depends(get_db), request: Request = None) -> TermService:
    svc = TermService(db)
    svc.request = request
    return svc


async def create_term(payload: TermCreate, svc: TermService = Depends(get_service)) -> TermOut:
    term = await svc.create(payload)
    return success_response(term, message="Term created successfully", schema=TermOut)


async def list_terms(svc: TermService = Depends(get_service)) -> list[TermOut]:
    payload = await svc.list()
    return success_response(payload, message="Terms retrieved successfully", schema=TermOut)


async def get_term(global_id: str, svc: TermService = Depends(get_service)) -> TermOut:
    term = await svc.get_by_global_id(global_id)
    return success_response(term, message="Term retrieved successfully", schema=TermOut)


async def update_term(global_id: str, payload: TermUpdate, svc: TermService = Depends(get_service)) -> TermOut:
    term = await svc.update_by_global_id(global_id, payload)
    return success_response(term, message="Term updated successfully", schema=TermOut)


async def set_active_term(global_id: str, payload: ActiveUpdate, svc: TermService = Depends(get_service)) -> TermOut:
    term = await svc.set_status_by_global_id(global_id, payload.value)
    return success_response(term, message="Term activation status updated successfully", schema=TermOut)


async def delete_term(global_id: str, svc: TermService = Depends(get_service)) -> None:
    term = await svc.set_status_by_global_id(global_id, 2)
    return success_response(term, message="Term deleted successfully", schema=TermOut)

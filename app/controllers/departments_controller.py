import json
from fastapi import Depends, Request, Query
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.department_service import DepartmentService
from app.schemas.department import DepartmentCreate, DepartmentOut, DepartmentsPage, DepartmentUpdate, ActiveUpdate
from app.api.response import success_response
from fastapi import Request

def get_service(db: AsyncSession = Depends(get_db), request: Request = None) -> DepartmentService:
    svc = DepartmentService(db)
    # attach request so BaseService.list may read query params directly
    svc.request = request
    return svc

async def create_department(payload: DepartmentCreate, svc: DepartmentService = Depends(get_service)) -> DepartmentOut:
    department = await svc.create(payload)
    return success_response(department, message="Department created successfully", schema=DepartmentOut)

async def list_departments(svc: DepartmentService = Depends(get_service)) -> list[DepartmentOut]:
    payload = await svc.list()
    return success_response(payload, message="Departments retrieved successfully", schema=DepartmentOut)

async def get_department(global_id: str, svc: DepartmentService = Depends(get_service)) -> DepartmentOut:
    department = await svc.get_by_global_id(global_id)
    return success_response(department, message="Department retrieved successfully", schema=DepartmentOut)

async def update_department(global_id: str, payload: DepartmentUpdate, svc: DepartmentService = Depends(get_service)) -> DepartmentOut:
    department = await svc.update_by_global_id(global_id, payload)
    return success_response(department, message="Department updated successfully", schema=DepartmentOut)

async def set_active_department(global_id: str, payload: ActiveUpdate, svc: DepartmentService = Depends(get_service)) -> DepartmentOut:
    department = await svc.set_status_by_global_id(global_id, payload.value)
    return success_response(department, message="Department activation status updated successfully", schema=DepartmentOut)

async def delete_department(global_id: str, svc: DepartmentService = Depends(get_service)) -> None:
    department = await svc.set_status_by_global_id(global_id, 2)
    return success_response(department, message="department deleted successfully", schema=DepartmentOut)
# app/api/v1/admins_router.py
from fastapi import APIRouter, Depends, status
from app.schemas.department import DepartmentCreate, DepartmentOut, DepartmentsPage, DepartmentUpdate, ActiveUpdate
from app.controllers import departments_controller as ctl
from app.api import auth as api_auth

router = APIRouter(
    tags=["departments"],
)

# List departments (lecturer only)
@router.get("/", response_model=DepartmentsPage, dependencies=[api_auth.lecturer])
async def list_departments(out=Depends(ctl.list_departments)):
    return out

# Get single department (lecturer only)
@router.get("/{global_id}", response_model=DepartmentOut, dependencies=[api_auth.lecturer])
async def get_department(global_id: str, out=Depends(ctl.get_department)):
    return out

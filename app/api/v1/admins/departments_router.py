# app/api/v1/admins_router.py
from fastapi import APIRouter, Depends, status
from app.schemas.department import DepartmentCreate, DepartmentOut, DepartmentsPage, DepartmentUpdate, ActiveUpdate
from app.controllers import departments_controller as ctl
from app.api import auth as api_auth

router = APIRouter(
    tags=["departments"],
)

# Create department (superadmin only)
@router.post("/", response_model=DepartmentOut, status_code=status.HTTP_201_CREATED, dependencies=[api_auth.superadmin])
async def create_department(payload: DepartmentCreate, out=Depends(ctl.create_department)):
    return out

# List departments (admin or superadmin)
@router.get("/", response_model=DepartmentsPage, dependencies=[api_auth.admins])
async def list_departments(out=Depends(ctl.list_departments)):
    return out

# Get single department (admin or superadmin)
@router.get("/{global_id}", response_model=DepartmentOut, dependencies=[api_auth.admins])
async def get_department(global_id: str, out=Depends(ctl.get_department)):
    return out

# Update department (superadmin only)
@router.patch("/{global_id}", response_model=DepartmentOut, dependencies=[api_auth.superadmin])
async def update_department(global_id: str, payload: DepartmentUpdate, out=Depends(ctl.update_department)):
    return out

@router.post("/{global_id}/status", response_model=DepartmentOut, dependencies=[api_auth.superadmin])
async def set_active(global_id: str, payload: ActiveUpdate, out=Depends(ctl.set_active_department)):
    return out

@router.post("/{global_id}/delete", response_model=DepartmentOut, dependencies=[api_auth.superadmin])
async def delete_department(global_id: str, out=Depends(ctl.delete_department)):
    return out
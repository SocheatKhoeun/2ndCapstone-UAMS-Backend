# app/api/v1/lecturers/lecturer_route.py
from fastapi import APIRouter, Depends, Query, status
from app.schemas.admin import AdminCreate, AdminUpdate, AdminOut, AdminsPage, ActiveUpdate
from app.controllers import admins_controller as ctl
from app.api import auth as api_auth

router = APIRouter(
    tags=["lecturers"],
)

# List admins (lecturer)
# @router.get("/", response_model=AdminsPage, dependencies=[api_auth.lecturer])
# async def list_admins(out=Depends(ctl.list_admins)):
#     return out

# Get single admin (lecturer)
# @router.get("/{global_id}", response_model=AdminOut, dependencies=[api_auth.lecturer])
# async def get_admin(global_id: str, out=Depends(ctl.get_admin)):
#     return out


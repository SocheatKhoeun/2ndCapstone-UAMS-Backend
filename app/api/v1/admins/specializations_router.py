# app/api/v1/admins_router.py
from fastapi import APIRouter, Depends, status
from typing import Optional
from app.schemas.specialization import SpecializationCreate, SpecializationOut, SpecializationsPage, SpecializationUpdate, ActiveUpdate
from app.controllers import specialization_controller as ctl
from app.api import auth as api_auth

router = APIRouter(
    tags=["specializations"],
)

# Create specialization (superadmin only)
@router.post("/", response_model=SpecializationOut, status_code=status.HTTP_201_CREATED, dependencies=[api_auth.superadmin])
async def create_specialization(out=Depends(ctl.create_specialization)):
    return out

# List specializations (admin or superadmin)
@router.get("/", response_model=SpecializationsPage, dependencies=[api_auth.admins])
async def list_specializations(out=Depends(ctl.list_specializations)):
    return out

# Get single specialization (admin or superadmin)
@router.get("/{global_id}", response_model=SpecializationOut, dependencies=[api_auth.admins])
async def get_specialization(global_id: str, out=Depends(ctl.get_specialization)):
    return out

# Update specialization (superadmin only)
@router.patch("/{global_id}", response_model=SpecializationOut, dependencies=[api_auth.superadmin])
async def update_specialization(global_id: str, out=Depends(ctl.update_specialization)):
    return out

@router.post("/{global_id}/status", response_model=SpecializationOut, dependencies=[api_auth.superadmin])
async def set_active(global_id: str, payload: ActiveUpdate, out=Depends(ctl.set_active_specialization)):
    return out

@router.post("/{global_id}/delete", response_model=SpecializationOut, dependencies=[api_auth.superadmin])
async def delete_specialization(global_id: str, out=Depends(ctl.delete_specialization)):
    return out
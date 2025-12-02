# app/api/v1/admins_router.py
from fastapi import APIRouter, Depends, status
from typing import Optional
from app.schemas.specialization import SpecializationCreate, SpecializationOut, SpecializationsPage, SpecializationUpdate, ActiveUpdate
from app.controllers import specialization_controller as ctl
from app.api import auth as api_auth

router = APIRouter(
    tags=["specializations"],
)

# List specializations (lecturer only)
@router.get("/", response_model=SpecializationsPage, dependencies=[api_auth.lecturer])
async def list_specializations(out=Depends(ctl.list_specializations)):
    return out

# Get single specialization (lecturer only)
@router.get("/{global_id}", response_model=SpecializationOut, dependencies=[api_auth.lecturer])
async def get_specialization(global_id: str, out=Depends(ctl.get_specialization)):
    return out

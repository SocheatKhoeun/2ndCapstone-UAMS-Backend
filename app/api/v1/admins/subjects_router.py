# app/api/v1/admins_router.py
from fastapi import APIRouter, Depends, Query, status, Response
from typing import Optional
from app.schemas.subject import SubjectCreate, SubjectOut, SubjectsPage, SubjectUpdate, ActiveUpdate
from app.controllers import subjects_controller as ctl
from app.api import auth as api_auth

router = APIRouter(
    tags=["subjects"],
)

# Create subject (superadmin only)
@router.post("/", response_model=SubjectOut, status_code=status.HTTP_201_CREATED, dependencies=[api_auth.admins])
async def create_subject(payload: SubjectCreate, out=Depends(ctl.create_subject)):
    return out

# List subjects (admin or superadmin)
@router.get("/", response_model=SubjectsPage, dependencies=[api_auth.admins])
async def list_subjects(out=Depends(ctl.list_subjects)):
    return out

# Get single subject (admin or superadmin)
@router.get("/{global_id}", response_model=SubjectOut, dependencies=[api_auth.admins])
async def get_subject(global_id: str, out=Depends(ctl.get_subject)):
    return out

# Update subject (superadmin only)
@router.patch("/{global_id}", response_model=SubjectOut, dependencies=[api_auth.admins])
async def update_subject(global_id: str, payload: SubjectUpdate, out=Depends(ctl.update_subject)):
    return out

@router.post("/{global_id}/status", response_model=SubjectOut, dependencies=[api_auth.admins])
async def set_active(global_id: str, payload: ActiveUpdate, out=Depends(ctl.set_active_subject)):
    return out

@router.post("/{global_id}/delete", response_model=SubjectOut, dependencies=[api_auth.superadmin])
async def delete_subject(global_id: str, out=Depends(ctl.delete_subject)):
    return out

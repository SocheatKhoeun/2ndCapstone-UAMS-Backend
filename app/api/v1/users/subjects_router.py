# app/api/v1/admins_router.py
from fastapi import APIRouter, Depends, Query, status, Response
from typing import Optional
from app.schemas.subject import SubjectCreate, SubjectOut, SubjectsPage, SubjectUpdate, ActiveUpdate
from app.controllers import subjects_controller as ctl
from app.api import auth as api_auth

router = APIRouter(
    tags=["subjects"],
)

# List subjects (User only)
@router.get("/", response_model=SubjectsPage, status_code=status.HTTP_201_CREATED)
async def list_subjects(out=Depends(ctl.list_subjects)):
    return out

# Get single subject (User only)
@router.get("/{global_id}", response_model=SubjectOut, status_code=status.HTTP_201_CREATED)
async def get_subject(global_id: str, out=Depends(ctl.get_subject)):
    return out

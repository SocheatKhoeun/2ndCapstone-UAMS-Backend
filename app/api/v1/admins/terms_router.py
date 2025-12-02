from fastapi import APIRouter, Depends, Query, status
from app.schemas.term import TermCreate, TermOut, TermsPage, TermUpdate, ActiveUpdate
from app.controllers import terms_controller as ctl
from app.api import auth as api_auth

router = APIRouter(
    tags=["terms"],
)


# Create term (admin only)
@router.post("/", response_model=TermOut, status_code=status.HTTP_201_CREATED, dependencies=[api_auth.admins])
async def create_term(payload: TermCreate, out=Depends(ctl.create_term)):
    return out


# List terms (admin or superadmin)
@router.get("/", response_model=TermsPage, dependencies=[api_auth.admins])
async def list_terms(out=Depends(ctl.list_terms)):
    return out


# Get single term (admin or superadmin)
@router.get("/{global_id}", response_model=TermOut, dependencies=[api_auth.admins])
async def get_term(global_id: str, out=Depends(ctl.get_term)):
    return out


# Update term (admin only)
@router.patch("/{global_id}", response_model=TermOut, dependencies=[api_auth.admins])
async def update_term(global_id: str, payload: TermUpdate, out=Depends(ctl.update_term)):
    return out


@router.post("/{global_id}/status", response_model=TermOut, dependencies=[api_auth.admins])
async def set_active(global_id: str, payload: ActiveUpdate, out=Depends(ctl.set_active_term)):
    return out


@router.post("/{global_id}/delete", response_model=TermOut, dependencies=[api_auth.admins])
async def delete_term(global_id: str, out=Depends(ctl.delete_term)):
    return out

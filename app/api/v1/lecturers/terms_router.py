from fastapi import APIRouter, Depends, Query, status
from app.schemas.term import TermCreate, TermOut, TermsPage, TermUpdate, ActiveUpdate
from app.controllers import terms_controller as ctl
from app.api import auth as api_auth

router = APIRouter(
    tags=["terms"],
)

# List terms (lecturer only)
@router.get("/", response_model=TermsPage, dependencies=[api_auth.lecturer])
async def list_terms(out=Depends(ctl.list_terms)):
    return out

# Get single term (lecturer only)
@router.get("/{global_id}", response_model=TermOut, dependencies=[api_auth.lecturer])
async def get_term(global_id: str, out=Depends(ctl.get_term)):
    return out

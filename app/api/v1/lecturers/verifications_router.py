from fastapi import APIRouter, Depends, status
from app.controllers import verification_controller as ctl
from app.schemas.verification import VerificationCreate, VerificationOut, VerificationsPage, VerificationUpdate
from app.api import auth as api_auth

router = APIRouter(
    tags=["verifications"],
)


@router.post("/", response_model=VerificationOut, status_code=status.HTTP_201_CREATED, dependencies=[api_auth.lecturer])
async def create_verification(out=Depends(ctl.create_verification)):
    return out

@router.get("/", response_model=VerificationsPage, dependencies=[api_auth.lecturer])
async def list_verifications(out=Depends(ctl.list_verifications)):
    return out


@router.get("/{global_id}", response_model=VerificationOut, dependencies=[api_auth.lecturer])
async def get_verification(global_id: str, out=Depends(ctl.get_verification)):
    return out


@router.patch("/{global_id}", response_model=VerificationOut, dependencies=[api_auth.lecturer])
async def update_verification(global_id: str, out=Depends(ctl.update_verification)):
    return out

@router.post("/{global_id}/status", response_model=VerificationOut, dependencies=[api_auth.lecturer])
async def set_active_verification(global_id: str, payload: dict, out=Depends(ctl.set_active_verification)):
    return out


@router.post("/{global_id}/delete", response_model=VerificationOut, dependencies=[api_auth.lecturer])
async def delete_verification(global_id: str, out=Depends(ctl.delete_verification)):
    return out

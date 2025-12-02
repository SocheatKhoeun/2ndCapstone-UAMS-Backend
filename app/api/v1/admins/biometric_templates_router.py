from fastapi import APIRouter, Depends, status
from app.schemas.biometric_template import BiometricTemplateCreate, BiometricTemplateOut, BiometricTemplatesPage, BiometricTemplateUpdate
from app.controllers import biometric_templates_controller as ctl
from app.api import auth as api_auth

router = APIRouter(
    tags=["biometric_templates"],
)


@router.post("/", response_model=BiometricTemplateOut, status_code=status.HTTP_201_CREATED, dependencies=[api_auth.admins])
async def create_biometric_template(out=Depends(ctl.create_biometric_template)):
    return out


@router.get("/", response_model=BiometricTemplatesPage, dependencies=[api_auth.admins])
async def list_biometric_templates(out=Depends(ctl.list_biometric_templates)):
    return out


@router.get("/{global_id}", response_model=BiometricTemplateOut, dependencies=[api_auth.admins])
async def get_biometric_template(global_id: str, out=Depends(ctl.get_biometric_template)):
    return out


@router.patch("/{global_id}", response_model=BiometricTemplateOut, dependencies=[api_auth.admins])
async def update_biometric_template(global_id: str, out=Depends(ctl.update_biometric_template)):
    return out


@router.post("/{global_id}/status", response_model=BiometricTemplateOut, dependencies=[api_auth.admins])
async def set_active_biometric_template(global_id: str, payload: dict, out=Depends(ctl.set_active_biometric_template)):
    return out


@router.post("/{global_id}/delete", response_model=BiometricTemplateOut, dependencies=[api_auth.admins])
async def delete_biometric_template(global_id: str, out=Depends(ctl.delete_biometric_template)):
    return out

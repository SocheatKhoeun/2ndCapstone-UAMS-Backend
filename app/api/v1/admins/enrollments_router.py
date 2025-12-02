from fastapi import APIRouter, Depends, status
from app.schemas.enrollment import EnrollmentCreate, EnrollmentOut, EnrollmentsPage, EnrollmentUpdate, ActiveUpdate
from app.controllers import enrollments_controller as ctl
from app.api import auth as api_auth

router = APIRouter(
    tags=["enrollments"],
)

@router.post("/", response_model=EnrollmentOut, status_code=status.HTTP_201_CREATED, dependencies=[api_auth.admins])
async def create_enrollment(out=Depends(ctl.create_enrollment)):
    return out

@router.get("/", response_model=EnrollmentsPage, dependencies=[api_auth.admins])
async def list_enrollments(out=Depends(ctl.list_enrollments)):
    return out

@router.get("/{global_id}", response_model=EnrollmentOut, dependencies=[api_auth.admins])
async def get_enrollment(global_id: str, out=Depends(ctl.get_enrollment)):
    return out

@router.patch("/{global_id}", response_model=EnrollmentOut, dependencies=[api_auth.admins])
async def update_enrollment(global_id: str, out=Depends(ctl.update_enrollment)):
    return out

@router.post("/{global_id}/status", response_model=EnrollmentOut, dependencies=[api_auth.admins])
async def set_active_enrollment(global_id: str, payload: ActiveUpdate, out=Depends(ctl.set_active_enrollment)):
    return out

@router.post("/{global_id}/delete", response_model=EnrollmentOut, dependencies=[api_auth.admins])
async def delete_enrollment(global_id: str, out=Depends(ctl.delete_enrollment)):
    return out

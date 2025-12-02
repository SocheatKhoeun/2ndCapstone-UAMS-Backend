from fastapi import APIRouter, Depends, status
from app.controllers import attendance_controller as ctl
from app.schemas.attendance import AttendanceCreate, AttendanceOut, AttendancesPage, AttendanceUpdate
from app.api import auth as api_auth

router = APIRouter(
    tags=["attendance"],
)


@router.post("/", response_model=AttendanceOut, status_code=status.HTTP_201_CREATED, dependencies=[api_auth.admins])
async def create_attendance(out=Depends(ctl.create_attendance)):
    return out


@router.get("/", response_model=AttendancesPage, dependencies=[api_auth.admins])
async def list_attendances(out=Depends(ctl.list_attendances)):
    return out


@router.get("/{global_id}", response_model=AttendanceOut, dependencies=[api_auth.admins])
async def get_attendance(global_id: str, out=Depends(ctl.get_attendance)):
    return out


@router.patch("/{global_id}", response_model=AttendanceOut, dependencies=[api_auth.admins])
async def update_attendance(global_id: str, out=Depends(ctl.update_attendance)):
    return out

@router.post("/{global_id}/status", response_model=AttendanceOut, dependencies=[api_auth.admins])
async def update_active_status(global_id: str, out=Depends(ctl.update_active_status)):
    return out


@router.post("/{global_id}/delete", response_model=AttendanceOut, dependencies=[api_auth.admins])
async def delete_attendance(global_id: str, out=Depends(ctl.delete_attendance)):
    return out

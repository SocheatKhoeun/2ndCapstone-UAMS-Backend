from fastapi import APIRouter, Depends, status
from app.controllers import attendance_controller as ctl
from app.schemas.attendance import AttendanceCreate, AttendanceOut, AttendancesPage, AttendanceUpdate
from app.api import auth as api_auth

router = APIRouter(
    tags=["attendance"],
)

# Create attendance (lecturer only)
@router.post("/", response_model=AttendanceCreate, status_code=status.HTTP_201_CREATED, dependencies=[api_auth.lecturer])
async def create_attendance(out=Depends(ctl.create_attendance)):
    return out

# List attendances (lecturer only)
@router.get("/", response_model=AttendancesPage, dependencies=[api_auth.lecturer])
async def list_attendances(out=Depends(ctl.list_attendances)):
    return out

# Get single attendance (lecturer only)
@router.get("/{global_id}", response_model=AttendanceOut, dependencies=[api_auth.lecturer])
async def get_attendance(global_id: str, out=Depends(ctl.get_attendance)):
    return out

# Update attendance (lecturer only)
@router.patch("/{global_id}", response_model=AttendanceOut, dependencies=[api_auth.lecturer])
async def update_attendance(global_id: str, out=Depends(ctl.update_attendance)):
    return out

# Update active status (lecturer only)
@router.post("/{global_id}/status", response_model=AttendanceOut, dependencies=[api_auth.lecturer])
async def update_active_status(global_id: str, out=Depends(ctl.update_active_status)):
    return out

# Delete attendance (lecturer only)
@router.post("/{global_id}/delete", response_model=AttendanceOut, dependencies=[api_auth.lecturer])
async def delete_attendance(global_id: str, out=Depends(ctl.delete_attendance)):
    return out

from fastapi import APIRouter, Depends, status
from app.controllers import attendance_controller as ctl
from app.schemas.attendance import AttendanceCreate, AttendanceOut, AttendancesPage, AttendanceUpdate
from app.api import auth as api_auth

router = APIRouter(
    tags=["attendance"],
)

# Create attendance (User only)
@router.post("/", response_model=AttendanceCreate, status_code=status.HTTP_201_CREATED)
async def create_attendance(out=Depends(ctl.create_attendance)):
    return out

# List attendances (User only)
@router.get("/", response_model=AttendancesPage, status_code=status.HTTP_201_CREATED)
async def list_attendances(out=Depends(ctl.list_attendances)):
    return out

# Get single attendance (User only)
@router.get("/{global_id}", response_model=AttendanceOut, status_code=status.HTTP_201_CREATED)
async def get_attendance(global_id: str, out=Depends(ctl.get_attendance)):
    return out

# Update attendance (User only)
@router.patch("/{global_id}", response_model=AttendanceOut, status_code=status.HTTP_201_CREATED)
async def update_attendance(global_id: str, out=Depends(ctl.update_attendance)):
    return out

# Update active status (User only)
@router.post("/{global_id}/status", response_model=AttendanceOut, status_code=status.HTTP_201_CREATED)
async def update_active_status(global_id: str, out=Depends(ctl.update_active_status)):
    return out


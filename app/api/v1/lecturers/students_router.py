from fastapi import APIRouter, Depends, Query, status, Response
from app.schemas.student import StudentCreate, StudentUpdate, StudentOut, ActiveUpdate
from app.controllers import students_controller as ctl
from app.api import auth as api_auth

router = APIRouter(tags=["students"])

# List students (lecturer only)
@router.get("/", response_model=list[StudentOut], dependencies=[api_auth.lecturer])
async def list_students(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    out=Depends(ctl.list_students),
):
    return out

# Get single student (lecturer only)
@router.get("/{global_id}", response_model=StudentOut, dependencies=[api_auth.lecturer])
async def get_student(global_id: str, out=Depends(ctl.get_student)):
    return out

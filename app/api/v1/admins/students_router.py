from fastapi import APIRouter, Depends, Query, status, Response
from app.schemas.student import StudentCreate, StudentUpdate, StudentOut, ActiveUpdate
from app.controllers import students_controller as ctl
from app.api import auth as api_auth

router = APIRouter(tags=["students"])


@router.post("/", response_model=StudentOut, status_code=status.HTTP_201_CREATED, dependencies=[api_auth.admins])
async def create_student(payload: StudentCreate, out=Depends(ctl.create_student)):
    return out


@router.get("/", response_model=list[StudentOut], dependencies=[api_auth.admins])
async def list_students(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    out=Depends(ctl.list_students),
):
    return out


@router.get("/{global_id}", response_model=StudentOut, dependencies=[api_auth.admins])
async def get_student(global_id: str, out=Depends(ctl.get_student)):
    return out


@router.patch("/{global_id}", response_model=StudentOut, dependencies=[api_auth.admins])
async def update_student(global_id: str, payload: StudentUpdate, out=Depends(ctl.update_student)):
    return out

@router.post("/{global_id}/status", response_model=StudentOut, dependencies=[api_auth.admins])
async def set_active_student(global_id: str, payload: ActiveUpdate, out=Depends(ctl.set_active_student)):
    return out

@router.delete("/{global_id}/delete", status_code=status.HTTP_204_NO_CONTENT, dependencies=[api_auth.superadmin])
async def delete_student(global_id: str, _=Depends(ctl.delete_student)):
    return Response(status_code=status.HTTP_204_NO_CONTENT)

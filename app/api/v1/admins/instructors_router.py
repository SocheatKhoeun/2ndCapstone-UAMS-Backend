from fastapi import APIRouter, Depends, status
from app.schemas.instructor import InstructorCreate, InstructorUpdate, InstructorOut
from app.controllers import instructors_controller as ctl
from app.api import auth as api_auth

router = APIRouter(tags=["instructors"])


@router.post("/", response_model=InstructorOut, status_code=status.HTTP_201_CREATED, dependencies=[api_auth.superadmin])
async def create_instructor(payload: InstructorCreate, out=Depends(ctl.create_instructor)):
    return out


@router.get("/", response_model=list[InstructorOut], dependencies=[api_auth.admins])
async def list_instructors(out=Depends(ctl.list_instructors)):
    return out


@router.get("/{global_id}", response_model=InstructorOut, dependencies=[api_auth.admins])
async def get_instructor(global_id: str, out=Depends(ctl.get_instructor)):
    return out


@router.patch("/{global_id}", response_model=InstructorOut, dependencies=[api_auth.superadmin])
async def update_instructor(global_id: str, payload: InstructorUpdate, out=Depends(ctl.update_instructor)):
    return out

@router.post("/{global_id}/status", response_model=InstructorOut, dependencies=[api_auth.superadmin])
async def set_active_instructor(global_id: str, payload: dict, out=Depends(ctl.set_active_instructor)):
    return out


# @router.delete("/{global_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[api_auth.superadmin])
# async def delete_instructor(global_id: str, _=Depends(ctl.delete_instructor)):
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

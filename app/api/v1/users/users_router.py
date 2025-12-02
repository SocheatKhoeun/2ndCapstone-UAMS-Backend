from fastapi import APIRouter, Depends, Query, status, Response
from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.controllers import users_controller as ctl

router = APIRouter(tags=["users"])

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate, out=Depends(ctl.create_user)):
    return out

@router.get("/", response_model=list[UserOut])
async def list_users(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    out=Depends(ctl.list_users),
):
    return out

@router.get("/{global_id}", response_model=UserOut)
async def get_user(global_id: str, out=Depends(ctl.get_user)):
    return out

@router.patch("/{global_id}", response_model=UserOut)
async def update_user(global_id: str, payload: UserUpdate, out=Depends(ctl.update_user)):
    return out

@router.delete("/{global_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(global_id: str, _=Depends(ctl.delete_user)):
    return Response(status_code=status.HTTP_204_NO_CONTENT)

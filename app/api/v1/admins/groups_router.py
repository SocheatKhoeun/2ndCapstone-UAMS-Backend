from fastapi import APIRouter, Depends, Query, status
from app.schemas.group import GroupCreate, GroupOut, GroupsPage, GroupUpdate, ActiveUpdate
from app.controllers import groups_controller as ctl
from app.api import auth as api_auth

router = APIRouter(
    tags=["groups"],
)


# Create group (admin only)
@router.post("/", response_model=GroupOut, status_code=status.HTTP_201_CREATED, dependencies=[api_auth.admins])
async def create_group(payload: GroupCreate, out=Depends(ctl.create_group)):
    return out


# List groups (admin or superadmin)
@router.get("/", response_model=GroupsPage, dependencies=[api_auth.admins])
async def list_groups(out=Depends(ctl.list_groups)):
    return out


# Get single group (admin or superadmin)
@router.get("/{global_id}", response_model=GroupOut, dependencies=[api_auth.admins])
async def get_group(global_id: str, out=Depends(ctl.get_group)):
    return out


# Update group (admin only)
@router.patch("/{global_id}", response_model=GroupOut, dependencies=[api_auth.admins])
async def update_group(global_id: str, payload: GroupUpdate, out=Depends(ctl.update_group)):
    return out


@router.post("/{global_id}/status", response_model=GroupOut, dependencies=[api_auth.admins])
async def set_active(global_id: str, payload: ActiveUpdate, out=Depends(ctl.set_active_group)):
    return out


@router.post("/{global_id}/delete", response_model=GroupOut, dependencies=[api_auth.admins])
async def delete_group(global_id: str, out=Depends(ctl.delete_group)):
    return out

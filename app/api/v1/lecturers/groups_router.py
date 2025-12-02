from fastapi import APIRouter, Depends, Query, status
from app.schemas.group import GroupCreate, GroupOut, GroupsPage, GroupUpdate, ActiveUpdate
from app.controllers import groups_controller as ctl
from app.api import auth as api_auth

router = APIRouter(
    tags=["groups"],
)

# List groups (lecturer only)
@router.get("/", response_model=GroupsPage, dependencies=[api_auth.lecturer])
async def list_groups(out=Depends(ctl.list_groups)):
    return out

# Get single group (lecturer only)
@router.get("/{global_id}", response_model=GroupOut, dependencies=[api_auth.lecturer])
async def get_group(global_id: str, out=Depends(ctl.get_group)):
    return out

from fastapi import APIRouter, Depends, Query, status
from app.schemas.group import GroupCreate, GroupOut, GroupsPage, GroupUpdate, ActiveUpdate
from app.controllers import groups_controller as ctl
from app.api import auth as api_auth

router = APIRouter(
    tags=["groups"],
)

# List groups (user only)
@router.get("/", response_model=GroupsPage, status_code=status.HTTP_201_CREATED)
async def list_groups(out=Depends(ctl.list_groups)):
    return out

# Get single group (user only)
@router.get("/{global_id}", response_model=GroupOut, status_code=status.HTTP_201_CREATED)
async def get_group(global_id: str, out=Depends(ctl.get_group)):
    return out

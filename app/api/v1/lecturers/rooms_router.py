from fastapi import APIRouter, Depends, Query, status
from app.schemas.room import RoomCreate, RoomOut, RoomsPage, RoomUpdate, ActiveUpdate
from app.controllers import rooms_controller as ctl
from app.api import auth as api_auth

router = APIRouter(
    tags=["rooms"],
)

# Create room (lecturer only)
# @router.post("/", response_model=RoomOut, status_code=status.HTTP_201_CREATED, dependencies=[Depends(api_auth.require_roles_claims(["lecturer"]))])
# async def create_room(payload: RoomCreate, out=Depends(ctl.create_room)):
#     return out


# List rooms (lecturer only)
@router.get("/", response_model=RoomsPage, dependencies=[Depends(api_auth.require_roles_claims(["lecturer"]))])
async def list_rooms(out=Depends(ctl.list_rooms)):
    return out


# Get single room (lecturer only)
@router.get("/{global_id}", response_model=RoomOut, dependencies=[Depends(api_auth.require_roles_claims(["lecturer"]))])
async def get_room(global_id: str, out=Depends(ctl.get_room)):
    return out


# Update room (lecturer only)
# @router.patch("/{global_id}", response_model=RoomOut, dependencies=[Depends(api_auth.require_roles_claims(["lecturer"]))])
# async def update_room(global_id: str, payload: RoomUpdate, out=Depends(ctl.update_room)):
#     return out


# @router.post("/{global_id}/status", response_model=RoomOut, dependencies=[Depends(api_auth.require_roles_claims(["lecturer"]))])
# async def set_active(global_id: str, payload: ActiveUpdate, out=Depends(ctl.set_active_room)):
#     return out

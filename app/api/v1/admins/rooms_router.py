from fastapi import APIRouter, Depends, Query, status
from app.schemas.room import RoomCreate, RoomOut, RoomsPage, RoomUpdate, ActiveUpdate
from app.controllers import rooms_controller as ctl
from app.api import auth as api_auth

router = APIRouter(
    tags=["rooms"],
)


# Create room (admin only)
@router.post("/", response_model=RoomOut, status_code=status.HTTP_201_CREATED, dependencies=[api_auth.admins])
async def create_room(payload: RoomCreate, out=Depends(ctl.create_room)):
    return out


# List rooms (admin or superadmin)
@router.get("/", response_model=RoomsPage, dependencies=[api_auth.admins])
async def list_rooms(out=Depends(ctl.list_rooms)):
    return out


# Get single room (admin or superadmin)
@router.get("/{global_id}", response_model=RoomOut, dependencies=[api_auth.admins])
async def get_room(global_id: str, out=Depends(ctl.get_room)):
    return out


# Update room (admin only)
@router.patch("/{global_id}", response_model=RoomOut, dependencies=[api_auth.admins])
async def update_room(global_id: str, payload: RoomUpdate, out=Depends(ctl.update_room)):
    return out


@router.post("/{global_id}/status", response_model=RoomOut, dependencies=[api_auth.admins])
async def set_active(global_id: str, payload: ActiveUpdate, out=Depends(ctl.set_active_room)):
    return out


@router.post("/{global_id}/delete", response_model=RoomOut, dependencies=[api_auth.admins])
async def delete_room(global_id: str, out=Depends(ctl.delete_room)):
    return out

from fastapi import APIRouter, Depends, Query, status
from app.schemas.room import RoomCreate, RoomOut, RoomsPage, RoomUpdate, ActiveUpdate
from app.controllers import rooms_controller as ctl
from app.api import auth as api_auth

router = APIRouter(
    tags=["rooms"],
)

# List rooms (User only)
@router.get("/", response_model=RoomsPage, status_code=status.HTTP_201_CREATED)
async def list_rooms(out=Depends(ctl.list_rooms)):
    return out

# Get single room (User only)
@router.get("/{global_id}", response_model=RoomOut, status_code=status.HTTP_201_CREATED)
async def get_room(global_id: str, out=Depends(ctl.get_room)):
    return out

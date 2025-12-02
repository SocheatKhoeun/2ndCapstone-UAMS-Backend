from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.room_service import RoomService
from app.schemas.room import RoomCreate, RoomOut, RoomsPage, RoomUpdate, ActiveUpdate
from app.api.response import success_response


def get_service(db: AsyncSession = Depends(get_db), request: Request = None) -> RoomService:
    svc = RoomService(db)
    svc.request = request
    return svc


async def create_room(payload: RoomCreate, svc: RoomService = Depends(get_service)) -> RoomOut:
    room = await svc.create(payload)
    return success_response(room, message="Room created successfully", schema=RoomOut)


async def list_rooms(svc: RoomService = Depends(get_service)) -> list[RoomOut]:
    rooms = await svc.list()
    return success_response(rooms, message="Rooms retrieved successfully", schema=RoomOut)


async def get_room(global_id: str, svc: RoomService = Depends(get_service)) -> RoomOut:
    room = await svc.get_by_global_id(global_id)
    return success_response(room, message="Room retrieved successfully", schema=RoomOut)


async def update_room(global_id: str, payload: RoomUpdate, svc: RoomService = Depends(get_service)) -> RoomOut:
    room = await svc.update_by_global_id(global_id, payload)
    return success_response(room, message="Room updated successfully", schema=RoomOut)


async def set_active_room(global_id: str, payload: ActiveUpdate, svc: RoomService = Depends(get_service)) -> RoomOut:
    room = await svc.set_status_by_global_id(global_id, payload.value)
    return success_response(room, message="Room activation status updated successfully", schema=RoomOut)


async def delete_room(global_id: str, svc: RoomService = Depends(get_service)) -> None:
    room = await svc.set_status_by_global_id(global_id, 2)
    return success_response(room, message="Room deleted successfully", schema=RoomOut)

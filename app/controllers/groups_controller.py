from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.group_service import GroupService
from app.schemas.group import GroupCreate, GroupOut, GroupsPage, GroupUpdate, ActiveUpdate
from app.api.response import success_response


def get_service(db: AsyncSession = Depends(get_db), request: Request = None) -> GroupService:
    svc = GroupService(db)
    svc.request = request
    return svc


async def create_group(payload: GroupCreate, svc: GroupService = Depends(get_service)) -> GroupOut:
    group = await svc.create(payload)
    return success_response(group, message="Group created successfully", schema=GroupOut)


async def list_groups(svc: GroupService = Depends(get_service)) -> list[GroupOut]:
    groups = await svc.list()
    return success_response(groups, message="Groups retrieved successfully", schema=GroupOut)


async def get_group(global_id: str, svc: GroupService = Depends(get_service)) -> GroupOut:
    group = await svc.get_by_global_id(global_id)
    return success_response(group, message="Group retrieved successfully", schema=GroupOut)


async def update_group(global_id: str, payload: GroupUpdate, svc: GroupService = Depends(get_service)) -> GroupOut:
    group = await svc.update_by_global_id(global_id, payload)
    return success_response(group, message="Group updated successfully", schema=GroupOut)


async def set_active_group(global_id: str, payload: ActiveUpdate, svc: GroupService = Depends(get_service)) -> GroupOut:
    group = await svc.set_status_by_global_id(global_id, payload.value)
    return success_response(group, message="Group activation status updated successfully", schema=GroupOut)


async def delete_group(global_id: str, svc: GroupService = Depends(get_service)) -> None:
    group = await svc.set_status_by_global_id(global_id, 2)
    return success_response(group, message="Group deleted successfully", schema=GroupOut)

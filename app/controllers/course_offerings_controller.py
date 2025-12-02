from fastapi import Depends, Request
from app.api.deps_helpers import resolve_body_and_fk
from app.models.group import Group
from app.models.subject import Subject
from app.models.term import Term
from app.models.instructor import Instructor
from app.models.room import Room
from app.models.generation import Generation
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.course_offering_service import CourseOfferingService
from app.schemas.course_offering import (
    CourseOfferingCreate,
    CourseOfferingOut,
    CourseOfferingsPage,
    CourseOfferingUpdate,
    ActiveUpdate,
)
from app.api.response import success_response


def get_service(db: AsyncSession = Depends(get_db), request: Request = None) -> CourseOfferingService:
    svc = CourseOfferingService(db)
    svc.request = request
    return svc


async def create_course_offering(
    payload: CourseOfferingCreate = Depends(resolve_body_and_fk(CourseOfferingCreate, {
        "group_id": Group,
        "subject_id": Subject,
        "term_id": Term,
        "instructor_id": Instructor,
        "assistant_id": Instructor,
        "room_id": Room,
        "generation_id": Generation,
    })),
    svc: CourseOfferingService = Depends(get_service),
) -> CourseOfferingOut:
    obj = await svc.create(payload)
    return success_response(obj, message="Course offering created successfully", schema=CourseOfferingOut)


async def list_course_offerings(svc: CourseOfferingService = Depends(get_service)) -> list[CourseOfferingOut]:
    objs = await svc.list()
    return success_response(objs, message="Course offerings retrieved successfully", schema=CourseOfferingOut)


async def get_course_offering(global_id: str, svc: CourseOfferingService = Depends(get_service)) -> CourseOfferingOut:
    obj = await svc.get_by_global_id(global_id)
    return success_response(obj, message="Course offering retrieved successfully", schema=CourseOfferingOut)


async def update_course_offering(
    global_id: str,
    payload: CourseOfferingUpdate = Depends(resolve_body_and_fk(CourseOfferingUpdate, {
        "group_id": Group,
        "subject_id": Subject,
        "term_id": Term,
        "instructor_id": Instructor,
        "assistant_id": Instructor,
        "room_id": Room,
        "generation_id": Generation,
    })),
    svc: CourseOfferingService = Depends(get_service),
) -> CourseOfferingOut:
    obj = await svc.update_by_global_id(global_id, payload)
    return success_response(obj, message="Course offering updated successfully", schema=CourseOfferingOut)


async def set_active_course_offering(global_id: str, payload: ActiveUpdate, svc: CourseOfferingService = Depends(get_service)) -> CourseOfferingOut:
    obj = await svc.set_status_by_global_id(global_id, payload.value)
    return success_response(obj, message="Course offering activation status updated successfully", schema=CourseOfferingOut)


async def delete_course_offering(global_id: str, svc: CourseOfferingService = Depends(get_service)) -> None:
    obj = await svc.set_status_by_global_id(global_id, 2)
    return success_response(obj, message="Course offering deleted successfully", schema=CourseOfferingOut)

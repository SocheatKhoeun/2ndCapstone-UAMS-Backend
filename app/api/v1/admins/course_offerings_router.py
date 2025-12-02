from fastapi import APIRouter, Depends, status
from app.schemas.course_offering import (
    CourseOfferingCreate,
    CourseOfferingOut,
    CourseOfferingsPage,
    CourseOfferingUpdate,
    ActiveUpdate,
)
from app.controllers import course_offerings_controller as ctl
from app.api import auth as api_auth

router = APIRouter(
    tags=["course_offerings"],
)


# Create (admin only)
@router.post("/", response_model=CourseOfferingOut, status_code=status.HTTP_201_CREATED, dependencies=[api_auth.admins])
async def create_course_offering(out=Depends(ctl.create_course_offering)):
    return out


# List (admin or superadmin)
@router.get("/", response_model=CourseOfferingsPage, dependencies=[api_auth.admins])
async def list_course_offerings(out=Depends(ctl.list_course_offerings)):
    return out


# Get single
@router.get("/{global_id}", response_model=CourseOfferingOut, dependencies=[api_auth.admins])
async def get_course_offering(global_id: str, out=Depends(ctl.get_course_offering)):
    return out


# Update (admin only)
@router.patch("/{global_id}", response_model=CourseOfferingOut, dependencies=[api_auth.admins])
async def update_course_offering(global_id: str, out=Depends(ctl.update_course_offering)):
    return out


@router.post("/{global_id}/status", response_model=CourseOfferingOut, dependencies=[api_auth.admins])
async def set_active(global_id: str, payload: ActiveUpdate, out=Depends(ctl.set_active_course_offering)):
    return out


@router.post("/{global_id}/delete", response_model=CourseOfferingOut, dependencies=[api_auth.admins])
async def delete_course_offering(global_id: str, out=Depends(ctl.delete_course_offering)):
    return out

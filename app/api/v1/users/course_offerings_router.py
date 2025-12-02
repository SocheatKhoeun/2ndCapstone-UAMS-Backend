from fastapi import APIRouter, Depends, status
from app.schemas.course_offering import (CourseOfferingOut, CourseOfferingsPage)
from app.controllers import course_offerings_controller as ctl
from app.api import auth as api_auth

router = APIRouter(
    tags=["course_offerings"],
)

# List (admin or superadmin)
@router.get("/", response_model=CourseOfferingsPage, status_code=status.HTTP_201_CREATED)
async def list_course_offerings(out=Depends(ctl.list_course_offerings)):
    return out

# Get single
@router.get("/{global_id}", response_model=CourseOfferingOut, status_code=status.HTTP_201_CREATED)
async def get_course_offering(global_id: str, out=Depends(ctl.get_course_offering)):
    return out

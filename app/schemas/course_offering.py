from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class CourseOfferingCreate(BaseModel):
    global_id: Optional[str] = None
    group_id: int
    subject_id: int
    term_id: int
    # accept either `room_id` or legacy `room` key from clients
    room_id: Optional[int] = None
    room: Optional[int] = None
    instructor_id: Optional[int] = None
    assistant_id: Optional[int] = None
    generation_id: int
    description: Optional[str] = None
    status: Optional[int] = None
    active: Optional[bool] = True
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class CourseOfferingUpdate(BaseModel):
    group_id: Optional[int] = None
    subject_id: Optional[int] = None
    term_id: Optional[int] = None
    room_id: Optional[int] = None
    room: Optional[int] = None
    instructor_id: int
    assistant_id: int
    generation_id: Optional[int] = None
    description: Optional[str] = None
    status: Optional[int] = None
    active: Optional[bool] = True
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class CourseOfferingOut(BaseModel):
    id: int
    global_id: str
    group_id: int
    subject_id: int
    term_id: int
    room_id: Optional[int] = None
    instructor_id: int
    assistant_id: int
    generation_id: Optional[int] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[int] = None
    active: Optional[bool] = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class CourseOfferingsPage(BaseModel):
    items: list[CourseOfferingOut]
    total: int
    page: int
    per_page: int
    total_pages: int
    next_page: Optional[int] = None
    prev_page: Optional[int] = None

    model_config = {"from_attributes": True}


class ActiveUpdate(BaseModel):
    value: int = Field(..., ge=0, le=1, description="0=inactive,1=active")
    model_config = {"from_attributes": True}

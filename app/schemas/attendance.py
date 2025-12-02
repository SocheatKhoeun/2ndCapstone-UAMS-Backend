from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class AttendanceCreate(BaseModel):
    session_id: Optional[int] = None
    student_id: Optional[int] = None
    status: Optional[str] = None
    checkin_time: Optional[datetime] = None
    method: Optional[str] = None
    verification_id: Optional[int] = None
    remarks: Optional[str] = None


class AttendanceUpdate(BaseModel):
    session_id: Optional[int] = None
    student_id: Optional[int] = None
    status: Optional[str] = None
    checkin_time: Optional[datetime] = None
    method: Optional[str] = None
    verification_id: Optional[int] = None
    remarks: Optional[str] = None
    active: Optional[bool] = True


class AttendanceOut(BaseModel):
    id: int
    global_id: str
    session_id: int
    student_id: int
    status: Optional[str] = None
    checkin_time: Optional[datetime] = None
    method: Optional[str] = None
    verification_id: Optional[int] = None
    remarks: Optional[str] = None
    active: Optional[bool] = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class AttendancesPage(BaseModel):
    items: list[AttendanceOut]
    total: int
    page: int
    per_page: int
    total_pages: int
    next_page: Optional[int] = None
    prev_page: Optional[int] = None

    model_config = {"from_attributes": True}

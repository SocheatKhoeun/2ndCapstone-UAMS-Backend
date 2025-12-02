from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class EnrollmentCreate(BaseModel):
    global_id: Optional[str] = None
    student_id: int
    offering_id: int
    status: Optional[int] = None
    enrolled_at: Optional[datetime] = None
    dropped_at: Optional[datetime] = None
    active: Optional[bool] = True

class EnrollmentUpdate(BaseModel):
    student_id: Optional[int] = None
    offering_id: Optional[int] = None
    status: Optional[int] = None
    enrolled_at: Optional[datetime] = None
    dropped_at: Optional[datetime] = None
    active: Optional[bool] = True

class EnrollmentOut(BaseModel):
    id: int
    global_id: str
    student_id: int
    offering_id: int
    status: Optional[int] = None
    enrolled_at: Optional[datetime] = None
    dropped_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    active: Optional[bool] = True
    
    model_config = {"from_attributes": True}

class EnrollmentsPage(BaseModel):
    items: list[EnrollmentOut]
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

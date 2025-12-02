from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class SubjectCreate(BaseModel):
    global_id: Optional[str] = None
    code: str
    specialization_id: int
    name: str
    description: Optional[str] = None
    credits: Optional[int] = None
    lecture_hours: Optional[int] = None
    lab_hours: Optional[int] = None
    active: Optional[bool] = True


class SubjectUpdate(BaseModel):
    code: str
    specialization_id: int
    name: str
    description: Optional[str] = None
    credits: Optional[int] = None
    lecture_hours: Optional[int] = None
    lab_hours: Optional[int] = None
    active: Optional[bool] = True


class SubjectOut(BaseModel):
    global_id: str
    code: str
    specialization_id: int
    name: str
    description: Optional[str] = None
    credits: Optional[int] = None
    lecture_hours: Optional[int] = None
    lab_hours: Optional[int] = None
    active: Optional[bool] = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class SubjectsPage(BaseModel):
    items: list[SubjectOut]
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

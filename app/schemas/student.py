from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date, datetime


class StudentBase(BaseModel):
    global_id: Optional[str] = None
    student_code: str
    first_name: Optional[str]
    last_name: Optional[str]
    gender: Optional[str]
    dob: Optional[date]
    email: EmailStr
    phone_number: Optional[str]
    address: Optional[str]
    profile_image: Optional[str]
    generation_id: Optional[int]
    active: Optional[int] = 1


class StudentCreate(StudentBase):
    password: str = Field(..., min_length=8, max_length=32)


class StudentUpdate(StudentBase):
    password: Optional[str] = Field(None, min_length=8, max_length=32)


class StudentOut(StudentBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class ActiveUpdate(BaseModel):
    value: int = Field(..., ge=0, le=1, description="0=inactive,1=active")
    model_config = {"from_attributes": True}
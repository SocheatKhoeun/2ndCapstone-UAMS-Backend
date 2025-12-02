from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class InstructorBase(BaseModel):
    global_id: Optional[str] = None
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr
    phone_number: Optional[str]
    position: Optional[str]
    active: Optional[int] = 1


class InstructorCreate(InstructorBase):
    password: str = Field(..., min_length=8, max_length=32)


class InstructorUpdate(InstructorBase):
    password: Optional[str] = Field(None, min_length=8, max_length=32)


class InstructorOut(InstructorBase):
    id: int
    global_id: str
    email: EmailStr
    phone_number: Optional[str]
    position: Optional[str]
    active: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
class ActiveUpdate(BaseModel):
    value: int = Field(..., ge=0, le=1, description="0=inactive,1=active")
    model_config = {"from_attributes": True}    

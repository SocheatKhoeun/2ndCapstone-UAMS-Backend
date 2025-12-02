from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class AdminCreate(BaseModel):
    global_id: Optional[str] = None
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=32)
    role: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    active: Optional[bool] = True


class AdminUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, max_length=32)
    role: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    active: Optional[bool] = None


class AdminOut(BaseModel):
    id: int
    global_id: str
    email: EmailStr
    role: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class AdminsPage(BaseModel):
    items: list[AdminOut]
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

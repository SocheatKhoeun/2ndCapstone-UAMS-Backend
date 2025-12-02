from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class SpecializationCreate(BaseModel):
    global_id: Optional[str] = None
    name: str
    department_id: int
    active: Optional[bool] = True

class SpecializationUpdate(BaseModel):
    name: Optional[str] = None
    department_id: int
    active: Optional[bool] = None

class SpecializationOut(BaseModel):
    id: int
    global_id: str
    name: str
    active: bool
    department_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    model_config = {"from_attributes": True}

class SpecializationsPage(BaseModel):
    items: list[SpecializationOut]
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

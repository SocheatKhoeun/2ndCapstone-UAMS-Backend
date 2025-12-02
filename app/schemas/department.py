from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class DepartmentCreate(BaseModel):
    global_id: Optional[str] = None
    name: str
    active: Optional[bool] = True

class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    active: Optional[bool] = None

class DepartmentOut(BaseModel):
    id: int
    global_id: str
    name: str
    active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    model_config = {"from_attributes": True}

class DepartmentsPage(BaseModel):
    items: list[DepartmentOut]
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

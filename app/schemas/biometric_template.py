from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class BiometricTemplateCreate(BaseModel):
    global_id: Optional[str] = None
    student_id: Optional[int] = None
    embedding: Optional[bytes] = None
    model: Optional[str] = None
    dimension: Optional[int] = None
    active: Optional[bool] = True


class BiometricTemplateUpdate(BaseModel):
    student_id: Optional[int] = None
    embedding: Optional[bytes] = None
    model: Optional[str] = None
    dimension: Optional[int] = None
    active: Optional[bool] = True


class BiometricTemplateOut(BaseModel):
    id: int
    global_id: str
    student_id: Optional[int] = None
    # embedding as bytes may be large; returning as-is. Consider returning a URL instead.
    embedding: Optional[bytes] = None
    model: Optional[str] = None
    dimension: Optional[int] = None
    active: Optional[bool] = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class BiometricTemplatesPage(BaseModel):
    items: list[BiometricTemplateOut]
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

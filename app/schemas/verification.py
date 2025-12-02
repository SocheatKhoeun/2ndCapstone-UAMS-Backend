from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class VerificationCreate(BaseModel):
    session_id: Optional[int] = None
    student_id: Optional[int] = None
    template_id: Optional[int] = None
    similarity: Optional[float] = None
    liveness_score: Optional[float] = None
    result: Optional[str] = None
    captured_image_url: Optional[str] = None


class VerificationUpdate(BaseModel):
    session_id: Optional[int] = None
    student_id: Optional[int] = None
    template_id: Optional[int] = None
    similarity: Optional[float] = None
    liveness_score: Optional[float] = None
    result: Optional[str] = None
    captured_image_url: Optional[str] = None
    active: Optional[bool] = True


class VerificationOut(BaseModel):
    id: int
    global_id: str
    session_id: Optional[int] = None
    student_id: Optional[int] = None
    template_id: Optional[int] = None
    similarity: Optional[float] = None
    liveness_score: Optional[float] = None
    result: Optional[str] = None
    captured_image_url: Optional[str] = None
    captured_at: Optional[datetime] = None
    active: Optional[bool] = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class VerificationsPage(BaseModel):
    items: list[VerificationOut]
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

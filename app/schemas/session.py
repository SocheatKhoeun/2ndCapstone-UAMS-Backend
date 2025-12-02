from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class SessionCreate(BaseModel):
    global_id: Optional[str] = None
    offering_id: int
    room_id: int
    start_datetime: datetime
    end_datetime: datetime
    status: Optional[str] = None
    active: Optional[bool] = True


class SessionUpdate(BaseModel):
    offering_id: Optional[int] = None
    room_id: Optional[int] = None
    start_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None
    status: Optional[str] = None
    active: Optional[bool] = None


class SessionOut(BaseModel):
    id: int
    global_id: str
    offering_id: int
    room_id: int
    start_datetime: datetime
    end_datetime: datetime
    status: Optional[str] = None
    active: Optional[bool] = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class SessionsPage(BaseModel):
    items: list[SessionOut]
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

from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class RoomCreate(BaseModel):
    global_id: Optional[str] = None
    room: str
    capacity: Optional[int] = None
    active: Optional[bool] = True


class RoomUpdate(BaseModel):
    room: str
    capacity: Optional[int] = None
    active: Optional[bool] = True


class RoomOut(BaseModel):
    id: int
    global_id: str
    room: str
    capacity: Optional[int] = None
    active: Optional[bool] = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class RoomsPage(BaseModel):
    items: list[RoomOut]
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

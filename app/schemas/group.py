from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from datetime import datetime


class GroupBase(BaseModel):
    group_name: str
    active: Optional[int] = 1


class GroupCreate(GroupBase):
    pass


class GroupUpdate(BaseModel):
    group_name: Optional[str]
    active: Optional[int]


class GroupOut(GroupBase):
    id: int
    global_id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        from_attributes = True


class GroupsPage(BaseModel):
    items: List[GroupOut]
    total: int

class ActiveUpdate(BaseModel):
    value: int = Field(..., ge=0, le=1, description="0=inactive,1=active")
    model_config = {"from_attributes": True}

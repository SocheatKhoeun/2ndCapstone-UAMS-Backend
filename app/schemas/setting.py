from typing import Optional
from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime


class SettingCreate(BaseModel):
    global_id: Optional[str] = Field(default_factory=lambda: str(uuid4()))
    key: str
    value: Optional[str] = None
    description: Optional[str] = None


class SettingUpdate(BaseModel):
    key: Optional[str] = None
    value: Optional[str] = None
    description: Optional[str] = None


class SettingOut(BaseModel):
    id: int
    global_id: Optional[str] = None
    key: str
    value: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}

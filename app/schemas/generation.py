from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class GenerationBase(BaseModel):
    global_id: Optional[str] = None
    generation: str = Field(..., min_length=1, max_length=255)
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    active: Optional[int] = 1


class GenerationCreate(GenerationBase):
    pass


class GenerationUpdate(GenerationBase):
    pass


class GenerationOut(GenerationBase):
    id: int
    global_id: str
    generation: str
    start_year: Optional[int]
    end_year: Optional[int]
    active: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class GenerationsPage(BaseModel):
    items: list[GenerationOut]
    total: int
    page: int
    per_page: int
    total_pages: int
    next_page: Optional[int] = None
    prev_page: Optional[int] = None

    class Config:
        orm_mode = True

class ActiveUpdate(BaseModel):
    value: int = Field(..., ge=0, le=1, description="0=inactive,1=active")
    model_config = {"from_attributes": True}
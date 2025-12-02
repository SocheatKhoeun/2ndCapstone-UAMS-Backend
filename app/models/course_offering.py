from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime, SmallInteger, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from uuid import uuid4


class CourseOffering(Base):
    __tablename__ = "course_offerings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    global_id: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False, default=lambda: str(uuid4()))
    group_id: Mapped[int] = mapped_column(nullable=False)
    subject_id: Mapped[int] = mapped_column(nullable=False)
    term_id: Mapped[int] = mapped_column(nullable=False)
    instructor_id: Mapped[int] = mapped_column(nullable=False)
    assistant_id: Mapped[int] = mapped_column(nullable=False)
    room_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    # generation_id is NOT NULL in the DB
    generation_id: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    # status values: 1=planned,2=active,3=completed,4=canceled
    status: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    # timestamp fields: use timezone-aware DateTime so times include timezone info
    start_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    end_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    active: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1)
    created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=True
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=True
    )

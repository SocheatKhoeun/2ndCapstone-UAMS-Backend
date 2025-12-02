from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime, SmallInteger, Integer, Enum as SAEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from uuid import uuid4


class Attendance(Base):
    __tablename__ = "attendance"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    global_id: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False, default=lambda: str(uuid4()))
    session_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=False)
    student_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=False)
    # Map to Postgres attendance_status enum
    status: Mapped[Optional[str]] = mapped_column(SAEnum(
        'present', 'late', 'absent', 'excused', name='attendance_status', native_enum=True
    ), nullable=True)
    checkin_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    # Map to Postgres attendance_method enum
    method: Mapped[Optional[str]] = mapped_column(SAEnum(
        'face', 'qr', 'manual', name='attendance_method', native_enum=True
    ), nullable=True)
    verification_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    remarks: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    active: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=True)

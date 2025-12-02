from datetime import date, datetime
from typing import Optional

from sqlalchemy import String, Date, DateTime, SmallInteger
from sqlalchemy.dialects.postgresql import ENUM as PG_ENUM
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from uuid import uuid4

class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    global_id: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False, default=lambda: str(uuid4()))
    student_code: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    gender: Mapped[Optional[str]] = mapped_column(
        PG_ENUM('male', 'female', 'other', name='gender_enum'), nullable=True
    )
    dob: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    # DB column `password` exists in schema; map attribute `hashed_password` to it
    hashed_password: Mapped[Optional[str]] = mapped_column(String(255), name="password", nullable=True)
    address: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    profile_image: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    generation_id: Mapped[Optional[int]] = mapped_column(nullable=True)
    active: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1)

    created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=True
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=True
    )

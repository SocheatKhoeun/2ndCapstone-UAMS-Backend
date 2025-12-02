from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime, SmallInteger
from sqlalchemy.dialects.postgresql import ENUM as PGEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from uuid import uuid4

class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    global_id: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False, default=lambda: str(uuid4()))
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    credits: Mapped[Optional[int]] = mapped_column(nullable=True)
    lecture_hours: Mapped[Optional[int]] = mapped_column(nullable=True)
    lab_hours: Mapped[Optional[int]] = mapped_column(nullable=True)
    specialization_id: Mapped[int] = mapped_column(nullable=False)
    active: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1)
    created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=True
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=True
    )
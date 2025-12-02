from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime, SmallInteger, Integer, Numeric, Enum as SAEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from uuid import uuid4


class Verification(Base):
    __tablename__ = "verifications"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    global_id: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False, default=lambda: str(uuid4()))
    session_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    student_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    template_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    similarity: Mapped[Optional[float]] = mapped_column(Numeric(5, 4), nullable=True)
    liveness_score: Mapped[Optional[float]] = mapped_column(Numeric(5, 4), nullable=True)
    # Map to Postgres enum `verification_result` for safe inserts/comparisons
    result: Mapped[Optional[str]] = mapped_column(SAEnum(
        'success', 'fail_match', 'fail_liveness', 'fail_quality', 'error', name='verification_result', native_enum=True
    ), nullable=True)
    captured_image_url: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    captured_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    active: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=True)

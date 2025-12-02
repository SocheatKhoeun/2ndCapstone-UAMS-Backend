from typing import Optional
from datetime import datetime
from sqlalchemy import SmallInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.db.base import Base
from uuid import uuid4


class Enrollment(Base):
    __tablename__ = "enrollments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    global_id: Mapped[str] = mapped_column(default=lambda: str(uuid4()), unique=True, index=True, nullable=False)
    student_id: Mapped[int] = mapped_column(nullable=False)
    offering_id: Mapped[int] = mapped_column(nullable=False)
    status: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    active: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1)
    enrolled_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    dropped_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=True)

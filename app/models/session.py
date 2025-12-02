from typing import Optional
from datetime import datetime
from sqlalchemy import DateTime, SmallInteger, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.db.base import Base
from uuid import uuid4


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    global_id: Mapped[str] = mapped_column(default=lambda: str(uuid4()), unique=True, index=True, nullable=False)
    offering_id: Mapped[int] = mapped_column(nullable=False)
    room_id: Mapped[int] = mapped_column(nullable=False)
    start_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    # Map to the Postgres ENUM type `session_status` defined in db/uams-v1.sql
    status: Mapped[Optional[str]] = mapped_column(SAEnum(
        'planned', 'completed', 'canceled', 'makeup', name='session_status', native_enum=True
    ), nullable=True)
    active: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=True)

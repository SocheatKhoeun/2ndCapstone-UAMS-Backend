from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime, SmallInteger, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from uuid import uuid4


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    global_id: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False, default=lambda: str(uuid4()))
    room: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    capacity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    active: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1)
    created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=True
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=True
    )

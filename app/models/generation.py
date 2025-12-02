from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime, SmallInteger
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from uuid import uuid4

class Generation(Base):
    __tablename__ = "generations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    global_id: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False, default=lambda: str(uuid4()))
    generation: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    start_year: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    end_year: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    active: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1)

    created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=True
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=True
    )

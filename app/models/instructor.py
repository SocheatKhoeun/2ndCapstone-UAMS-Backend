from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime, SmallInteger
from sqlalchemy.dialects.postgresql import ENUM as PGEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from uuid import uuid4

class Instructor(Base):
    __tablename__ = "instructors"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    global_id: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False, default=lambda: str(uuid4()))
    first_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    # DB column `password` exists in schema; map attribute `hashed_password` to it
    hashed_password: Mapped[Optional[str]] = mapped_column(String(255), name="password", nullable=True)
    # Quote the enum type name to avoid SQL parser errors when the type name
    # collides with SQL keywords (e.g., POSITION()). Quoting ensures the CAST
    # is emitted as ::"position" which PostgreSQL accepts.
    position: Mapped[str] = mapped_column(
        PGEnum("professor", "lecturer", "assistant", name="position", create_type=False, quote=True)
    )
    active: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1)

    created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=True
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=True
    )

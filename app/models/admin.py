from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime, SmallInteger
from sqlalchemy.dialects.postgresql import ENUM as PGEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from uuid import uuid4

class Admin(Base):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    global_id: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False, default=lambda: str(uuid4()))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    # DB column is named `password` in the SQL schema; map attribute `hashed_password` to that column
    hashed_password: Mapped[str] = mapped_column(String(255), name="password")
    # DB defines a custom enum type named `role`; map to that enum to avoid datatype mismatch
    role: Mapped[str] = mapped_column(
        PGEnum("superadmin", "admin", name="role", create_type=False)
    )
    first_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    # DB 'active' column is SMALLINT in the SQL schema; use SmallInteger to match
    active: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1)

    created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=True
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=True
    )

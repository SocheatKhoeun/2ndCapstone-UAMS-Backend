from sqlalchemy import Column, Integer, String, SmallInteger, DateTime
from sqlalchemy.sql import func
from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from uuid import uuid4

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    global_id: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False, default=lambda: str(uuid4()))
    group_name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    active = Column(SmallInteger, default=1)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

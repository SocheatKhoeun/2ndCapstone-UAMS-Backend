from typing import Sequence, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.subject import Subject
from app.schemas.subject import SubjectCreate, SubjectUpdate, SubjectOut, SubjectsPage, ActiveUpdate
from app.core.errors import DuplicateEmail, NotFound
from app.core.errors import InvalidPasswordLength
from passlib.context import CryptContext
from app.services.base_service import BaseService
import logging
from uuid import uuid4

_pwd = CryptContext(schemes=["pbkdf2_sha256", "bcrypt"], deprecated="auto")


class SubjectService(BaseService):
    """Business logic for Subjects. No FastAPI imports here."""
    model = Subject

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    async def create(self, payload: SubjectCreate) -> Subject:
        if await self.exists_by("code", payload.code):
            raise DuplicateEmail("Subject code already registered")
        subject = await super().create(payload.dict(exclude_unset=True))
        return subject
    
    async def update_by_global_id(self, global_id: str, payload: SubjectUpdate) -> Subject:
        obj = await self.get_by_global_id(global_id)
        # if changing Subject code, ensure uniqueness
        if payload.code and payload.code != obj.code:
            existing = await self.get_one_by("code", payload.code)
            if existing:
                raise DuplicateEmail("Subject code already registered")

        # Delegate the actual update logic to BaseService to avoid duplication
        return await super().update_by_global_id(global_id, payload)

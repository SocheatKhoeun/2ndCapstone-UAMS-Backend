from typing import Sequence, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.admin import Admin
from app.schemas.admin import AdminCreate, AdminUpdate
from app.core.errors import DuplicateEmail, NotFound
from app.core.errors import InvalidPasswordLength
from passlib.context import CryptContext
from app.services.base_service import BaseService
import logging
from uuid import uuid4

_pwd = CryptContext(schemes=["pbkdf2_sha256", "bcrypt"], deprecated="auto")


class AdminService(BaseService):
    """Business logic for admins. No FastAPI imports here."""
    model = Admin

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    async def create(self, payload: AdminCreate) -> Admin:
        if await self.exists_by("email", payload.email):
            raise DuplicateEmail("Email already registered")
        if payload.global_id and await self.exists_by("global_id", payload.global_id):
            raise DuplicateEmail("Global ID already registered")
        # hashing will be attempted below; map any hasher errors to domain errors

        # generate a global_id if not provided
        gid = payload.global_id or uuid4().hex
        admin = Admin(
            global_id=gid,
            email=payload.email,
            hashed_password=None,
            role=payload.role,
            first_name=payload.first_name,
            last_name=payload.last_name,
            # DB uses SMALLINT (1/0) for `active` — store as integer 1/0
            active=int(payload.active) if payload.active is not None else 1,
        )
        # perform hashing with explicit error mapping
        if payload.password is not None:
            # enforce application-level password policy: 8-32 characters
            if not (8 <= len(payload.password) <= 32):
                raise InvalidPasswordLength("Password must be between 8 and 32 characters")
            # log password metadata (length, type, masked prefix) to help diagnose hashing issues
            try:
                pw_bytes = payload.password.encode("utf-8")
                pw_len = len(pw_bytes)
                pw_type = type(payload.password).__name__
                prefix = (payload.password[:8] + "...") if len(payload.password) > 8 else payload.password
            except Exception:
                pw_len = None
                pw_type = None
                prefix = None
            logging.getLogger(__name__).info(
                "attempting to hash password: len=%s type=%s prefix=%s",
                pw_len,
                pw_type,
                prefix,
            )
            try:
                admin.hashed_password = _pwd.hash(payload.password)
            except ValueError:
                # passlib/bcrypt raised password-too-long or backend error
                raise InvalidPasswordLength(
                    "Password too long or invalid for the hasher; must be <= 72 bytes when encoded in UTF-8"
                )
        self.db.add(admin)
        await self.db.commit()
        await self.db.refresh(admin)
        return admin

    async def authenticate(self, email: str, password: str) -> Optional[Admin]:
        admin = await self.get_one_by("email", email)
        if not admin:
            return None
        try:
            if _pwd.verify(password, admin.hashed_password):
                return admin
        except ValueError:
            # treat hashing/verification errors as authentication failure
            return None
        return None

    # use BaseService.list() and BaseService.count() to avoid duplicated code

    async def update(self, global_id: str, payload: AdminUpdate) -> Admin:
        admin = await self._by_global_id(global_id)
        if not admin:
            raise NotFound("Admin not found")

        if payload.email and payload.email != admin.email:
            if await self._by_email(payload.email):
                raise DuplicateEmail("Email already registered")
            admin.email = payload.email

        if payload.password:
            # enforce application-level password policy: 8-32 characters
            if not (8 <= len(payload.password) <= 32):
                raise InvalidPasswordLength("Password must be between 8 and 32 characters")
            try:
                admin.hashed_password = _pwd.hash(payload.password)
            except ValueError:
                raise InvalidPasswordLength(
                    "Password too long or invalid for the hasher; must be <= 72 bytes when encoded in UTF-8"
                )

        if payload.role is not None:
            admin.role = payload.role

        if payload.first_name is not None:
            admin.first_name = payload.first_name

        if payload.last_name is not None:
            admin.last_name = payload.last_name

        if payload.active is not None:
            admin.active = payload.active

        await self.db.commit()
        await self.db.refresh(admin)
        return admin

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.instructor import Instructor
from typing import Optional
from app.core.errors import InvalidPasswordLength
from passlib.context import CryptContext

from app.core.errors import DuplicateEmail, DuplicatePhone, NotFound
from sqlalchemy import select
from app.services.base_service import BaseService

_pwd = CryptContext(schemes=["pbkdf2_sha256", "bcrypt"], deprecated="auto")


class InstructorService(BaseService):
    model = Instructor

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    async def create(self, payload):
        data = payload.dict()
        # enforce unique email and phone_number (avoid DB IntegrityError)
        if data.get("email"):
            q = await self.db.execute(select(Instructor).where(Instructor.email == data.get("email")))
            if q.scalar_one_or_none():
                raise DuplicateEmail("Email already registered")
        if data.get("phone_number"):
            q = await self.db.execute(select(Instructor).where(Instructor.phone_number == data.get("phone_number")))
            if q.scalar_one_or_none():
                raise DuplicatePhone("Phone number already registered")
        # handle password hashing
        if data.get("password"):
            if not (8 <= len(data["password"]) <= 32):
                raise InvalidPasswordLength("Password must be between 8 and 32 characters")
            try:
                data["hashed_password"] = _pwd.hash(data.pop("password"))
            except ValueError:
                raise InvalidPasswordLength(
                    "Password too long or invalid for the hasher; must be <= 72 bytes when encoded in UTF-8"
                )
        obj = Instructor(**data)
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def update(self, id: int, payload):
        obj = await self.get(id)
        for k, v in payload.dict().items():
            if k == "password" and v:
                if not (8 <= len(v) <= 32):
                    raise InvalidPasswordLength("Password must be between 8 and 32 characters")
                try:
                    obj.hashed_password = _pwd.hash(v)
                except ValueError:
                    raise InvalidPasswordLength(
                        "Password too long or invalid for the hasher; must be <= 72 bytes when encoded in UTF-8"
                    )
            elif k != "password":
                # if updating email/phone, ensure uniqueness
                if k == "email" and v and v != obj.email:
                    q = await self.db.execute(select(Instructor).where(Instructor.email == v))
                    if q.scalar_one_or_none():
                        raise DuplicateEmail("Email already registered")
                if k == "phone_number" and v and v != obj.phone_number:
                    q = await self.db.execute(select(Instructor).where(Instructor.phone_number == v))
                    if q.scalar_one_or_none():
                        raise DuplicatePhone("Phone number already registered")
                setattr(obj, k, v)
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def authenticate(self, email: str, password: str) -> Optional[Instructor]:
        """Authenticate an instructor by email and password. Returns the Instructor
        instance on success or None on failure."""
        q = await self.db.execute(select(Instructor).where(Instructor.email == email))
        inst = q.scalar_one_or_none()
        if not inst or not inst.hashed_password:
            return None
        try:
            if _pwd.verify(password, inst.hashed_password):
                return inst
        except Exception:
            # treat hashing/verification errors as authentication failure
            return None
        return None

    

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from app.models.student import Student
from sqlalchemy import text
from fastapi import HTTPException, status
from app.core.errors import InvalidPasswordLength
from passlib.context import CryptContext
from app.services.base_service import BaseService, generic_list, generic_count

_pwd = CryptContext(schemes=["pbkdf2_sha256", "bcrypt"], deprecated="auto")


class StudentService(BaseService):
    model = Student

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    async def create(self, payload):
        data = payload.dict()
        # enforce unique email, student_code and phone_number to avoid DB integrity errors
        if data.get("email"):
            q = await self.db.execute(select(Student).where(Student.email == data.get("email")))
            if q.scalar_one_or_none():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        if data.get("student_code"):
            q = await self.db.execute(select(Student).where(Student.student_code == data.get("student_code")))
            if q.scalar_one_or_none():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student code already registered")
        if data.get("phone_number"):
            q = await self.db.execute(select(Student).where(Student.phone_number == data.get("phone_number")))
            if q.scalar_one_or_none():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phone number already registered")
        gen_id = data.get("generation_id")
        # If a generation_id is provided, ensure it exists to avoid FK violation
        if gen_id is not None:
            q = text("SELECT 1 FROM generations WHERE id = :id")
            res = await self.db.execute(q.bindparams(id=gen_id))
            if res.first() is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"generation_id {gen_id} does not exist")

        # handle password hashing similarly to other services
        if data.get("password"):
            if not (8 <= len(data["password"]) <= 32):
                raise InvalidPasswordLength("Password must be between 8 and 32 characters")
            try:
                data["hashed_password"] = _pwd.hash(data.pop("password"))
            except ValueError:
                raise InvalidPasswordLength(
                    "Password too long or invalid for the hasher; must be <= 72 bytes when encoded in UTF-8"
                )

        obj = Student(**data)
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def update(self, global_id: int, payload):
        obj = await self.get_by_global_id(global_id)
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
                setattr(obj, k, v)
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj

    async def authenticate(self, email: str, password: str) -> Optional[Student]:
        """Authenticate a student by email and password. Returns the Student
        instance on success or None on failure."""
        q = await self.db.execute(select(Student).where(Student.email == email))
        stu = q.scalar_one_or_none()
        if not stu or not stu.hashed_password:
            return None
        try:
            if _pwd.verify(password, stu.hashed_password):
                return stu
        except Exception:
            return None
        return None
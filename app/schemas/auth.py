from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class Login(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=32)


class TokenOut(BaseModel):
    token: str
    expires: int
    role: str
    refresh_token: Optional[str] = None
    refresh_expires: Optional[int] = None


class RefreshRequest(BaseModel):
    refresh_token: str

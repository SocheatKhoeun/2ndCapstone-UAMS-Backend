from typing import Optional
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from app.utils.jwt_utils import create_access_token, decode_access_token
from app.schemas.auth import Login, TokenOut, RefreshRequest
from app.services.admin_service import AdminService
from app.services.instructor_service import InstructorService
from app.services.student_service import StudentService
from app.db.session import get_session
from app.api.deps import get_setting_from_cache
from app.core.config import settings
import app.api.auth as api_auth

logger = logging.getLogger(__name__)

router = APIRouter(tags=["auth"])

@router.post("/login", response_model=dict)
async def login(payload: Login, db=Depends(get_session), jwt_ttl: Optional[str] = Depends(get_setting_from_cache("jwt_ttl")), jwt_ttl_refresh: Optional[str] = Depends(get_setting_from_cache("jwt_ttl_refresh"))):
    # Try instructor login first
    inst_svc = InstructorService(db)
    instructor = await inst_svc.authenticate(payload.email, payload.password)
    if instructor:
        # map instructor position to role claim used across the app
        pos = (instructor.position or "").lower()
        role_map = {
            "professor": "professor",
            "lecturer": "lecturer",
            "assistant": "assistant",
        }
        role = role_map.get(pos, "lecturer")
        safe_user = {
            "user_id": instructor.id,
            "email": instructor.email,
            "role": role,
            "global_id": getattr(instructor, "global_id", None),
            "first_name": instructor.first_name,
            "last_name": instructor.last_name,
        }
    else:
        # Try student login
        stu_svc = StudentService(db)
        student = await stu_svc.authenticate(payload.email, payload.password)
        if not student:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        safe_user = {
            "user_id": student.id,
            "email": student.email,
            "role": "student",
            "global_id": getattr(student, "global_id", None) or getattr(student, "student_code", None),
            "first_name": student.first_name,
            "last_name": student.last_name,
        }
    # Use the environment-configured secret only
    secret = settings.JWT_PRIVATE
    if not secret:
        # Missing signing key is a server misconfiguration
        raise HTTPException(status_code=500, detail=("Server misconfiguration: missing JWT signing key"))

    # safe_user is prepared above for instructor or student

    # parse jwt_ttl if provided from settings cache; ensure integer TTL is passed
    ttl_value = 3600  # default to 1 hour if not set
    if jwt_ttl:
        try:
            ttl_value = int(jwt_ttl)
        except Exception:
            logger.warning("Invalid jwt_ttl in cache: %s; falling back to default", jwt_ttl)

    # create access and refresh tokens
    token, expire = create_access_token(safe_user, secret, ttl_value, token_type="access")
    # refresh TTL
    refresh_ttl_val = 60 * 60 * 24 * 7  # default 7 days
    if jwt_ttl_refresh:
        try:
            refresh_ttl_val = int(jwt_ttl_refresh)
        except Exception:
            logger.warning("Invalid jwt_ttl_refresh in cache: %s; falling back to default", jwt_ttl_refresh)
    refresh_token, refresh_expire = create_access_token(safe_user, secret, refresh_ttl_val, token_type="refresh")

    # Include role in the response for client convenience
    return {"status": "success", "data": {"token": token, "expires": expire, "role": safe_user.get("role"), "refresh_token": refresh_token, "refresh_expires": refresh_expire}}



@router.post("/refresh", response_model=dict,  dependencies=[api_auth.admins])
async def refresh_token(body: RefreshRequest, db=Depends(get_session), jwt_ttl: Optional[str] = Depends(get_setting_from_cache("jwt_ttl")), jwt_ttl_refresh: Optional[str] = Depends(get_setting_from_cache("jwt_ttl_refresh"))):
    """Accept a refresh token and return a new access token (and rotated refresh token)."""
    secret = settings.JWT_PRIVATE
    if not secret:
        raise HTTPException(status_code=500, detail="Server misconfiguration: missing JWT signing key")

    try:
        payload = decode_access_token(body.refresh_token, secret)
    except HTTPException as e:
        raise e

    # ensure token is a refresh token
    if not payload or payload.get("token_type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    # build new access token
    ttl_value = 3600
    if jwt_ttl:
        try:
            ttl_value = int(jwt_ttl)
        except Exception:
            logger.warning("Invalid jwt_ttl in cache: %s; falling back to default", jwt_ttl)

    access_token, access_exp = create_access_token(payload, secret, ttl_value, token_type="access")

    # rotate refresh token
    refresh_ttl_val = 60 * 60 * 24 * 7
    if jwt_ttl_refresh:
        try:
            refresh_ttl_val = int(jwt_ttl_refresh)
        except Exception:
            logger.warning("Invalid jwt_ttl_refresh in cache: %s; falling back to default", jwt_ttl_refresh)
    new_refresh, new_refresh_exp = create_access_token(payload, secret, refresh_ttl_val, token_type="refresh")

    return {"status": "success", "data": {"token": access_token, "expires": access_exp, "refresh_token": new_refresh, "refresh_expires": new_refresh_exp}}

from typing import Optional
import logging
from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.utils.jwt_utils import create_access_token, decode_access_token
from app.schemas.auth import Login, RefreshRequest
from app.services.admin_service import AdminService
from app.db.session import get_session
from app.api.deps import get_setting_from_cache
from app.core.config import settings
from app.api.deps import get_current_admin

logger = logging.getLogger(__name__)

router = APIRouter(tags=["auth"])

@router.post("/login")
async def login(payload: Login, db=Depends(get_session), jwt_ttl: Optional[str] = Depends(get_setting_from_cache("jwt_ttl"))):
    svc = AdminService(db)
    admin = await svc.authenticate(payload.email, payload.password)
    if not admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    # Use the environment-configured secret only
    secret = settings.JWT_PRIVATE
    if not secret:
        # Missing signing key is a server misconfiguration
        raise HTTPException(status_code=500, detail=("Server misconfiguration: missing JWT signing key"))

    safe_admin = {
        "user_id": admin.id,
        "email": admin.email,
        "role": admin.role,
        "global_id": admin.global_id,
        "first_name": admin.first_name,
        "last_name": admin.last_name,
        "token_type": "access",
    }
    # jwt_ttl is resolved by FastAPI via Depends and should be a string or None
    # parse jwt_ttl if provided from settings cache; ensure integer TTL is passed
    print(jwt_ttl)
    ttl_value = 3600  # default to 1 hour if not set
    if jwt_ttl:
        try:
            ttl_value = int(jwt_ttl)
        except Exception:
            logger.warning("Invalid jwt_ttl in cache: %s; falling back to default", jwt_ttl)

    token, expire = create_access_token(safe_admin, secret, ttl_value)

    return {"status": "success", "data": {"token": token, "expires": expire}}


@router.post("/refresh")

async def issue_refresh_token(claims: dict = Depends(get_current_admin), jwt_ttl_refresh: Optional[str] = Depends(get_setting_from_cache("jwt_ttl_refresh"))):
    """Issue a refresh token for the currently-authenticated admin.

    This endpoint requires a valid access token (Bearer) and returns a refresh token
    that the client can store and later present to the refresh endpoint.
    """
    secret = settings.JWT_PRIVATE
    if not secret:
        raise HTTPException(status_code=500, detail="Server misconfiguration: missing JWT signing key")

    # claims is the decoded token payload from get_current_admin
    payload = claims

    # rotate/generate refresh token TTL (default 7 days)
    refresh_ttl_val = 60 * 60 * 24 * 7
    if jwt_ttl_refresh:
        try:
            refresh_ttl_val = int(jwt_ttl_refresh)
        except Exception:
            logger.warning("Invalid jwt_ttl_refresh in cache: %s; falling back to default", jwt_ttl_refresh)

    refresh_token, refresh_exp = create_access_token(payload, secret, refresh_ttl_val, token_type="refresh")
    return {"status": "success", "data": {"refresh_token": refresh_token, "refresh_expires": refresh_exp}}
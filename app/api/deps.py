from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from typing import Optional
from app.services.setting_service import SettingService
from fastapi import Request
import logging

logger = logging.getLogger(__name__)


# async def get_setting_value(key: str, db: AsyncSession = Depends(get_session)) -> Optional[str]:
#     svc = SettingService(db)
#     setting = await svc.get_by_key(key)
#     return setting.value if setting else None


async def get_setting_from_db(key: str, db: AsyncSession = Depends(get_session)) -> Optional[str]:
    svc = SettingService(db)
    setting = await svc.get_by_key(key)
    logger.debug("get_setting_from_db key=%s -> %r", key, setting.value if setting else None)
    return setting.value if setting else None


# Simple in-memory cache for settings. Keys map to string values.
# This is intentionally minimal — suitable for local development and tests.
_SETTING_CACHE: dict = {}


def get_setting_from_cache(key: str):
    """Return a dependency that provides the setting value for `key`.

    Usage:
        jwt_private: str = Depends(get_setting_from_cache("jwt_private"))

    The returned dependency will first consult an in-memory cache. If missing,
    it will fetch from the DB using SettingService and populate the cache.
    """

    async def _dep(db: AsyncSession = Depends(get_session)) -> Optional[str]:
        # return cached value if present
        if key in _SETTING_CACHE:
            logger.debug("setting_cache hit for key=%s", key)
            return _SETTING_CACHE[key]

        # otherwise load from DB using BaseService helper get_one_by
        svc = SettingService(db)
        try:
            setting = await svc.get_one_by("key", key)
        except Exception:
            setting = None

        val = getattr(setting, "value", None) if setting else None
        if val is not None:
            _SETTING_CACHE[key] = val
            logger.debug("setting_cache set for key=%s -> %r", key, val)
        else:
            logger.debug("setting_cache miss for key=%s (not found)", key)
        return val

    return _dep

from fastapi import HTTPException, status
from app.utils.jwt_utils import decode_access_token
from app.core.config import settings


def get_current_admin(request: Request):
    """Dependency to require a Bearer JWT and return decoded claims.

    This is intentionally minimal: it does not perform a DB lookup. Routes that
    need the full Admin object can call AdminService themselves or add a small
    wrapper that looks up the user by id.
    """
    auth = request.headers.get("Authorization")
    if not auth:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Authorization header")
    parts = auth.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Authorization header")
    token = parts[1]

    secret = settings.JWT_PRIVATE
    if not secret:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server misconfiguration: missing JWT signing key")

    payload = decode_access_token(token, secret)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    return payload

async def get_db(session: AsyncSession = Depends(get_session)) -> AsyncSession:
    return session
from fastapi import Depends, HTTPException, status, Request
from typing import List
from app.api.deps import get_setting_from_cache
from app.db.session import get_session
from app.api.deps import get_current_admin
import logging
logger = logging.getLogger(__name__)

def require_roles_claims(allowed: List[str]):
    """Claims-only guard: inspects the token's role claim without DB lookup.

    Useful for admin endpoints that use a different user store (Admins).
    """
    def role_guard(claims: dict = Depends(get_current_admin)):
        role = claims.get("role")
        logger.debug("get_current_admin claims: %s", claims)
        if role not in allowed:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
        return claims

    return role_guard


# Convenience short-hands for common role deps so routes can be declared tersely.
from typing import List as _List


def role_dep(roles: _List[str]):
    """Return a FastAPI Depends object for the given role list.

    Usage:
        dependencies=[api_auth.role_dep(["admin","superadmin"])]
    or
        claims: dict = api_auth.admins
    """
    # don't print at import time; use logging instead
    logger.debug("creating role_dep for roles: %s", roles)
    return Depends(require_roles_claims(roles))


# Pre-made shorthands
admins = role_dep(["admin", "superadmin"])
superadmin = role_dep(["superadmin"])
lecturer = role_dep(["professor", "lecturer", "assistant"])


# -----------------------
# DB-backed guards for other user tables (lecturer/student)
# -----------------------
from typing import Callable
from fastapi import Request
from app.utils.jwt_utils import decode_access_token


def require_roles_model(allowed: List[str], service_cls: Callable, id_claim: str = "user_id"):
    """Factory that returns a dependency which:
    - decodes Bearer token
    - extracts id from token using id_claim (or sub/id)
    - loads entity via service_cls(db)
    - checks entity.role (or type) is in allowed

    Returns an async dependency function suitable for Depends()
    """

    async def _guard(request: Request, jwt_private: str = Depends(get_setting_from_cache("jwt_private")), db = Depends(get_session)):
        auth = request.headers.get("Authorization")
        if not auth:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Authorization header")
        parts = auth.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Authorization header")
        token = parts[1]

        try:
            payload = decode_access_token(token, jwt_private)
        except Exception:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        obj_id = payload.get(id_claim) or payload.get("sub") or payload.get("id")
        if not obj_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Malformed token (no id)")

        svc = service_cls(db)
        try:
            entity = await svc.get(int(obj_id))
        except Exception:
            entity = None

        if not entity:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")

        # If entity has a role attribute, enforce it; otherwise skip role check
        if getattr(entity, "role", None) not in allowed:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

        return entity

    return _guard


# Short helpers (assume services exist at app.services.instructor_service and student_service)
try:
    from app.services.instructor_service import InstructorService
except Exception:
    InstructorService = None

try:
    from app.services.student_service import StudentService
except Exception:
    StudentService = None


instructor_guard = Depends(require_roles_model(["instructor"], InstructorService)) if InstructorService else None
student_guard = Depends(require_roles_model(["student"], StudentService)) if StudentService else None

from fastapi import APIRouter, Depends

# Import routers (each module/package should expose an APIRouter named `router`)
from app.api.v1.users import router as users_router
from app.api.v1.admins import router as admins_router
from app.api.v1.lecturers import router as lecturers_router
from app.api.v1.admin_auth_router import router as admin_auth_router
from app.api.v1.admins.students_router import router as students_router
from app.api.v1.user_auth_router import router as user_auth_router
from app.api import auth as api_auth

api_router = APIRouter()

# Public auth endpoints (login) - add only login publicly and protect refresh
# Admin: map login and refresh (refresh requires valid access token)
admin_login = next((r for r in admin_auth_router.routes if getattr(r, "path", "").endswith("/login")), None)
admin_refresh = next((r for r in admin_auth_router.routes if getattr(r, "path", "").endswith("/refresh")), None)
if admin_login:
	api_router.add_api_route("/admin/login", endpoint=admin_login.endpoint, methods=getattr(admin_login, "methods", None), tags=["admin"])
if admin_refresh:
	# Mount refresh without requiring an active access token so clients can send only a refresh token
	api_router.add_api_route("/admin/auth/refresh", endpoint=admin_refresh.endpoint, methods=getattr(admin_refresh, "methods", None), tags=["admin"]) 

# User: expose only login publicly and protect refresh
user_login = next((r for r in user_auth_router.routes if getattr(r, "path", "").endswith("/login")), None)
user_refresh = next((r for r in user_auth_router.routes if getattr(r, "path", "").endswith("/refresh")), None)
if user_login:
	api_router.add_api_route("/user/login", endpoint=user_login.endpoint, methods=getattr(user_login, "methods", None), tags=["user"])
if user_refresh:
	# Mount user refresh without requiring current admin; accept refresh token in body/header
	api_router.add_api_route("/user/refresh", endpoint=user_refresh.endpoint, methods=getattr(user_refresh, "methods", None), tags=["user"])

# --- Protected endpoints ------------------------------------------------
# Admin routes: protect by role; allow both 'admin' and 'superadmin' for normal admin endpoints
api_router.include_router(
	admins_router,
	prefix="/admin/auth",
	dependencies=[Depends(api_auth.require_roles_claims(["admin", "superadmin"]))],
)

# Route lecturers
api_router.include_router(
    lecturers_router,
    prefix="/lecturer/auth",
    dependencies=[Depends(api_auth.require_roles_claims(["professor", "lecturer", "assistant"]))],
)

api_router.include_router(users_router, prefix="/user")
# Students (instructors are mounted under /admins/instructors)
api_router.include_router(students_router, prefix="/students")

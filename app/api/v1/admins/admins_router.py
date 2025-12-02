# app/api/v1/admins_router.py
from fastapi import APIRouter, Depends, Query, status
from app.schemas.admin import AdminCreate, AdminUpdate, AdminOut, AdminsPage, ActiveUpdate
from app.controllers import admins_controller as ctl
from app.api import auth as api_auth
from app.services.admin_service import AdminService
from app.api.response import success_response
from app.db.session import get_db  # keep naming consistent project-wide

router = APIRouter(
    tags=["admins"],
)

# Create admin (superadmin only)
@router.post("/", response_model=AdminOut, status_code=status.HTTP_201_CREATED, dependencies=[api_auth.superadmin])
async def create_admin(payload: AdminCreate, out=Depends(ctl.create_admin)):
    return out

# List admins (admin or superadmin)
@router.get("/", response_model=AdminsPage, dependencies=[api_auth.admins])
async def list_admins(out=Depends(ctl.list_admins)):
    return out

# Get single admin (admin or superadmin)
@router.get("/{global_id}", response_model=AdminOut, dependencies=[api_auth.admins])
async def get_admin(global_id: str, out=Depends(ctl.get_admin)):
    return out

# Update admin (superadmin only)
@router.patch("/{global_id}", response_model=AdminOut, dependencies=[api_auth.superadmin])
async def update_admin(global_id: str, payload: AdminUpdate, out=Depends(ctl.update_admin)):
    return out

@router.post("/{global_id}/status", response_model=AdminOut, dependencies=[api_auth.superadmin])
async def set_active(global_id: str, payload: ActiveUpdate, out=Depends(ctl.set_active_admin)):
    return out

# @router.post("/{global_id}/delete", response_model=AdminOut, dependencies=[api_auth.superadmin])
# async def delete_admin(global_id: str, out=Depends(ctl.delete_admin)):
#     return out

# Who am I (returns admin record for the current token holder)
@router.get("/me", response_model=AdminOut, dependencies=[api_auth.admins])
async def me(claims: dict = api_auth.admins, db=Depends(get_db)):
    admin_id = claims.get("user_id") or claims.get("sub") or claims.get("id")
    if not admin_id:
        # Your login code should put sub=user_id; adjust accordingly:
        # claims['sub'] = str(admin.id)
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Malformed token (no subject)")
    svc = AdminService(db)
    admin = await svc.get(int(admin_id))
    return success_response(admin, schema=AdminOut)

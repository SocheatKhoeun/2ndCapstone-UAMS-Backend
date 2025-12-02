from fastapi import APIRouter, Depends, status
from app.schemas.session import SessionCreate, SessionOut, SessionsPage, SessionUpdate
from app.controllers import sessions_controller as ctl
from app.api import auth as api_auth

router = APIRouter(
    tags=["sessions"],
)

# Create session
@router.post("/", response_model=SessionOut, status_code=status.HTTP_201_CREATED, dependencies=[api_auth.lecturer])
async def create_session(out=Depends(ctl.create_session)):
    return out

# List sessions (lecturer only)
@router.get("/", response_model=SessionsPage, dependencies=[api_auth.lecturer])
async def list_sessions(out=Depends(ctl.list_sessions)):
    return out

# Get single session (lecturer only)
@router.get("/{global_id}", response_model=SessionOut, dependencies=[api_auth.lecturer])
async def get_session(global_id: str, out=Depends(ctl.get_session)):
    return out

# Update session
@router.patch("/{global_id}", response_model=SessionOut, dependencies=[api_auth.lecturer])
async def update_session(global_id: str, out=Depends(ctl.update_session)):
    return out

# Update active status
@router.post("/{global_id}/status", response_model=SessionOut, dependencies=[api_auth.lecturer])
async def update_active_status(global_id: str, out=Depends(ctl.update_active_status)):
    return out

# Delete session
@router.post("/{global_id}/delete", response_model=SessionOut, dependencies=[api_auth.lecturer])
async def delete_session(global_id: str, out=Depends(ctl.delete_session)):
    return out
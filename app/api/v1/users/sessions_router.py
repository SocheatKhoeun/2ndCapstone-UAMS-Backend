from fastapi import APIRouter, Depends, status
from app.schemas.session import SessionCreate, SessionOut, SessionsPage, SessionUpdate
from app.controllers import sessions_controller as ctl
from app.api import auth as api_auth

router = APIRouter(
    tags=["sessions"],
)
# List sessions (User only)
@router.get("/", response_model=SessionsPage, status_code=status.HTTP_201_CREATED)
async def list_sessions(out=Depends(ctl.list_sessions)):
    return out

# Get single session (User only)
@router.get("/{global_id}", response_model=SessionOut, status_code=status.HTTP_201_CREATED)
async def get_session(global_id: str, out=Depends(ctl.get_session)):
    return out

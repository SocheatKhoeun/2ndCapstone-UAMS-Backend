from fastapi import APIRouter, Depends, Query, status
from app.schemas.generation import GenerationCreate, GenerationUpdate, GenerationOut, ActiveUpdate
from app.controllers import generation_controller as ctl
from app.api import auth as api_auth

router = APIRouter(tags=["generations"]) 

@router.post("/", response_model=GenerationOut, status_code=status.HTTP_201_CREATED, dependencies=[api_auth.superadmin])
async def create_generation(payload: GenerationCreate, out=Depends(ctl.create_generation)):
    return out

@router.get("/", response_model=list[GenerationOut], dependencies=[api_auth.admins])
async def list_generations(page: int = Query(1, ge=1), limit: int = Query(50, ge=1, le=200), out=Depends(ctl.list_generations)):
    return out

@router.get("/{global_id}", response_model=GenerationOut, dependencies=[api_auth.admins])
async def get_generation(global_id: str, out=Depends(ctl.get_generation)):
    return out

@router.patch("/{global_id}", response_model=GenerationOut, dependencies=[api_auth.superadmin])
async def update_generation(global_id: str, payload: GenerationUpdate, out=Depends(ctl.update_generation)):
    return out

@router.post("/{global_id}/status", response_model=GenerationOut, dependencies=[api_auth.superadmin])
async def set_active_generation(global_id: str, payload: ActiveUpdate, out=Depends(ctl.set_active_generation)):
    return out
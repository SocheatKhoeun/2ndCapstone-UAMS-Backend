from fastapi import APIRouter, Depends, Query, status
from app.schemas.generation import GenerationCreate, GenerationUpdate, GenerationOut, ActiveUpdate
from app.controllers import generation_controller as ctl
from app.api import auth as api_auth

router = APIRouter(tags=["generations"]) 

# List generations (lecturer only)
@router.get("/", response_model=list[GenerationOut], dependencies=[api_auth.lecturer])
async def list_generations(page: int = Query(1, ge=1), limit: int = Query(50, ge=1, le=200), out=Depends(ctl.list_generations)):
    return out

# Get single generation by global_id (lecturer only)
@router.get("/{global_id}", response_model=GenerationOut, dependencies=[api_auth.lecturer])
async def get_generation(global_id: str, out=Depends(ctl.get_generation)):
    return out

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.generation_service import GenerationService
from app.schemas.generation import ActiveUpdate, GenerationCreate, GenerationUpdate, GenerationOut, GenerationsPage
from app.api.response import success_response
from fastapi import Request

def get_service(db: AsyncSession = Depends(get_db), request: Request = None) -> GenerationService:
    svc = GenerationService(db)
    svc.request = request
    return svc

async def create_generation(payload: GenerationCreate, svc: GenerationService = Depends(get_service)) -> GenerationOut:
    generation = await svc.create(payload)
    return success_response(generation, message="Generation created")

async def list_generations(svc: GenerationService = Depends(get_service)) -> list[GenerationsPage]:
    payload = await svc.list()
    return success_response(payload, message="Generations retrieved successfully")

async def get_generation(global_id: str, svc: GenerationService = Depends(get_service)) -> GenerationOut:
    generation =  await svc.get_by_global_id(global_id)
    return success_response(generation, message="Generation retrieved successfully")

async def update_generation(global_id: str, payload: GenerationUpdate, svc: GenerationService = Depends(get_service)) -> GenerationOut:
    generation = await svc.update_by_global_id(global_id, payload)
    return success_response(generation, message="Generation updated successfully")

async def set_active_generation(global_id: str, payload: ActiveUpdate, svc: GenerationService = Depends(get_service)) -> GenerationOut:
    admin = await svc.set_status_by_global_id(global_id, payload.value)
    return success_response(admin, message="Generation activation status updated successfully")

async def delete_generation(global_id: str, svc: GenerationService = Depends(get_service)) -> None:
    admin = await svc.set_status_by_global_id(global_id, 2)
    return success_response(admin, message="Generation deleted successfully")
from fastapi import APIRouter, Depends, Query, status
from app.schemas.setting import SettingCreate, SettingUpdate, SettingOut
from app.controllers import settings_controller as ctl

router = APIRouter(tags=["settings"])


@router.post("/", response_model=SettingOut, status_code=status.HTTP_201_CREATED)
async def create_setting(payload: SettingCreate, out=Depends(ctl.create_setting)):
    return out

@router.get("/", response_model=list[SettingOut])
async def list_settings(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    out=Depends(ctl.list_settings),
):
    return out

@router.get("/{global_id}", response_model=SettingOut)
async def get_setting(global_id: str, out=Depends(ctl.get_setting)):
    return out

@router.patch("/{global_id}", response_model=SettingOut)
async def update_setting(global_id: str, payload: SettingUpdate, out=Depends(ctl.update_setting)):
    return out

@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh_settings_cache():
    # reload settings into app.state cache
    try:
        from app.main import _load_settings_into_cache

        await _load_settings_into_cache()
    except Exception as e:
        return {"status": "error", "message": str(e)}

    return {"status": "success", "message": "settings refreshed"}

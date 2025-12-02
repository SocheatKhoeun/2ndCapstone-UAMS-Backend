from typing import Any, Dict, Mapping
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException


async def resolve_fk_ids(db: AsyncSession, data: Dict[str, Any], mapping: Mapping[str, Any]) -> Dict[str, Any]:
    """Resolve fields in `data` using `mapping` where mapping maps field -> Model.

    If a value is an int or numeric string it will be used as-is. If it's a
    non-numeric string it will be treated as a `global_id` and the corresponding
    Model will be queried for the numeric `id`.

    Raises HTTPException(400) if referenced resource not found.
    """
    for key, Model in mapping.items():
        if key not in data:
            continue
        val = data.get(key)
        if val is None:
            continue
        if isinstance(val, int):
            continue
        if isinstance(val, str):
            s = val.strip()
            if s.isdigit():
                data[key] = int(s)
                continue
            q = select(Model.id).where(getattr(Model, "global_id") == s)
            result = await db.scalar(q)
            if not result:
                raise HTTPException(status_code=400, detail=f"{key} with global_id '{s}' not found")
            data[key] = int(result)
    return data

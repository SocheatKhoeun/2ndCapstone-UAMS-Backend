from typing import Callable, Dict, Any, Mapping
from fastapi import Depends, Body, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.utils.fk_resolver import resolve_fk_ids


def resolve_body_and_fk(schema_cls, fk_mapping: Mapping[str, Any]) -> Callable:
    """Return a dependency function which:
    - reads the raw request body explicitly (so FastAPI won't treat it as query)
    - resolves any FK global_ids to numeric ids using fk_mapping
    - returns a validated schema instance with resolved ids
    """

    async def _dep(body: dict = Body(...), db: AsyncSession = Depends(get_db)):
        # Body(...) forces FastAPI to take the JSON body; avoid None/query mistakes
        if body is None:
            raise HTTPException(status_code=422, detail="Request body is required")

        # Ensure we operate on a plain dict (don't validate with Pydantic yet)
        if not isinstance(body, dict):
            try:
                body = dict(body)
            except Exception:
                raise HTTPException(status_code=422, detail="Request body must be a JSON object")
       
        # Remove unset / null values to avoid passing them to the model
        data = {k: v for k, v in body.items() if v is not None}

        # Resolve FK global_ids -> numeric ids before Pydantic validation
        data = await resolve_fk_ids(db, data, fk_mapping)

        # Now validate/construct the Pydantic model with resolved ids
        return schema_cls(**data)

    return _dep

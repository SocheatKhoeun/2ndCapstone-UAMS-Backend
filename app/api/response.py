from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional, Type


def _to_schema(data, schema: Type):
    """Convert SQLAlchemy model(s) or pagination dict/list to Pydantic schema instances.

    Returns Pydantic model(s) or dict suitable for further json encoding.
    """
    def _get_schema_fields(sch: Type):
        # pydantic v2
        if hasattr(sch, "model_fields"):
            try:
                return set(sch.model_fields.keys())
            except Exception:
                pass
        # pydantic v1
        if hasattr(sch, "__fields__"):
            try:
                return set(sch.__fields__.keys())
            except Exception:
                pass
        return None

    def _convert_item(item, sch: Type):
        # try pydantic v2 API
        if hasattr(sch, "model_validate"):
            try:
                return sch.model_validate(item)
            except Exception:
                pass
        # try v1 from_orm
        if hasattr(sch, "from_orm"):
            try:
                return sch.from_orm(item)
            except Exception:
                pass
        # try v1 parse_obj
        if hasattr(sch, "parse_obj"):
            try:
                return sch.parse_obj(item)
            except Exception:
                pass
        # fallback: convert to primitives and filter by schema fields
        prim = jsonable_encoder(item)
        allowed = _get_schema_fields(sch)
        if allowed and isinstance(prim, dict):
            return {k: v for k, v in prim.items() if k in allowed}
        return prim

    # pagination dict
    if isinstance(data, dict) and "items" in data:
        items = data.get("items") or []
        converted = [_convert_item(i, schema) for i in items]
        out = dict(data)
        out["items"] = converted
        return out

    # list of models
    if isinstance(data, (list, tuple)):
        return [_convert_item(i, schema) for i in data]

    # single model
    return _convert_item(data, schema)


def success_response(data, message: Optional[str] = None, code: int = 200, schema: Optional[Type] = None):
    """Return a JSONResponse with a uniform wrapper. If `schema` is provided,
    convert model(s) to the schema first, then JSON-encode the result.
    """
    if schema is not None and data is not None:
        try:
            converted = _to_schema(data, schema)
            encoded = jsonable_encoder(converted)
            # filter encoded primitives to schema fields when possible
            allowed = None
            if hasattr(schema, "model_fields"):
                try:
                    allowed = set(schema.model_fields.keys())
                except Exception:
                    allowed = None
            elif hasattr(schema, "__fields__"):
                try:
                    allowed = set(schema.__fields__.keys())
                except Exception:
                    allowed = None

            if allowed is not None:
                # filter single dict
                if isinstance(encoded, dict) and "items" not in encoded:
                    encoded = {k: v for k, v in encoded.items() if k in allowed}
                # filter pagination dict items
                if isinstance(encoded, dict) and "items" in encoded and isinstance(encoded["items"], list):
                    filtered_items = []
                    for it in encoded["items"]:
                        if isinstance(it, dict):
                            filtered_items.append({k: v for k, v in it.items() if k in allowed})
                        else:
                            filtered_items.append(it)
                    encoded["items"] = filtered_items
                # filter list of dicts
                if isinstance(encoded, list):
                    new_list = []
                    for it in encoded:
                        if isinstance(it, dict):
                            new_list.append({k: v for k, v in it.items() if k in allowed})
                        else:
                            new_list.append(it)
                    encoded = new_list
        except Exception:
            # fallback to plain jsonable encoding if conversion fails
            encoded = jsonable_encoder(data)
    else:
        encoded = jsonable_encoder(data)

    return JSONResponse(status_code=code, content={"status": "success", "data": encoded, "message": message, "code": code})
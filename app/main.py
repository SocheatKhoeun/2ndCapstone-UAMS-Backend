from typing import Optional
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from app.core.config import settings
from app.core.logging import setup_logging
from app.api.v1.router import api_router
from app.services.setting_service import SettingService
from app.db.session import AsyncSessionLocal
import os
import time
from app.core.errors import DomainError, NotFound, DuplicateEmail, InvalidPasswordLength
from app.core.errors import DuplicatePhone
from fastapi.responses import JSONResponse
from fastapi import Request

setup_logging()
app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

# Ensure the process timezone is set to UTC. This sets the TZ environment variable and calls
# time.tzset() on Unix systems so that datetime.utcnow() and other time functions behave as UTC.
# Note: time.tzset() is not available on Windows.
os.environ.setdefault("TZ", "UTC")
try:
    # Some platforms require tzset() to apply TZ env var to the process
    time.tzset()
except Exception:
    # Non-fatal if tzset is unavailable
    pass

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def attach_settings_to_request(request, call_next):
    # expose settings cache on each request similar to req.setting in Express
    request.state.setting = getattr(request.app.state, "settings_cache", {})
    return await call_next(request)


def _wrap_response(status: str, data=None, message: Optional[str] = None, code: int = 200):
    return {"status": status, "data": data, "message": message, "code": code}


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    # exc.detail may already be a dict from FastAPI validation, handle gracefully
    detail = exc.detail if not isinstance(exc.detail, (list, dict)) else exc.detail
    return JSONResponse(status_code=exc.status_code, content=_wrap_response("error", data=None, message=str(detail), code=exc.status_code))


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content=_wrap_response("error", data=exc.errors(), message="Validation error", code=422))


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    # Log exception via standard logging (setup_logging configures logging)
    import logging

    logging.exception("Unhandled exception: %s", exc)
    return JSONResponse(status_code=HTTP_500_INTERNAL_SERVER_ERROR, content=_wrap_response("error", data=None, message="Internal server error", code=HTTP_500_INTERNAL_SERVER_ERROR))


@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError):
    # Map common domain errors to HTTP responses
    if isinstance(exc, NotFound):
        return JSONResponse(status_code=404, content=_wrap_response("error", data=None, message=str(exc), code=404))
    if isinstance(exc, DuplicateEmail):
        return JSONResponse(status_code=409, content=_wrap_response("error", data=None, message=str(exc), code=409))
    if isinstance(exc, DuplicatePhone):
        return JSONResponse(status_code=409, content=_wrap_response("error", data=None, message=str(exc), code=409))
    if isinstance(exc, InvalidPasswordLength):
        return JSONResponse(status_code=400, content=_wrap_response("error", data=None, message=str(exc), code=400))

    # Generic domain error
    return JSONResponse(status_code=400, content=_wrap_response("error", data=None, message=str(exc), code=400))


@app.middleware("http")
async def wrap_response_middleware(request: Request, call_next):
    """Middleware to wrap successful responses into a uniform structure.

    If the response is already a JSON with our structure, return it unchanged. Otherwise,
    put the original response body under `data` and set status="success".
    """
    response: Response = await call_next(request)

    # For non-JSON responses or streaming, return as-is
    if response.media_type != "application/json":
        return response

    try:
        raw_body = b""
        async for chunk in response.body_iterator:
            raw_body += chunk
    except Exception:
        # response.body_iterator not always available; fall back to returning response
        return response

    # Recreate response content
    import json

    try:
        payload = json.loads(raw_body)
    except Exception:
        return response

    # If already wrapped (has keys status and data), return as-is
    if isinstance(payload, dict) and "status" in payload and "data" in payload and "code" in payload:
        return JSONResponse(status_code=response.status_code, content=payload)

    wrapped = _wrap_response("success", data=payload, message=None, code=response.status_code)
    return JSONResponse(status_code=response.status_code, content=wrapped)


@app.get("/health", tags=["system"])
def health():
    # Return already-wrapped response so middleware returns it unchanged
    from fastapi.responses import JSONResponse

    return JSONResponse(status_code=200, content=_wrap_response("success", data={"status": "ok"}, message=None, code=200))


app.include_router(api_router, prefix=settings.API_V1_PREFIX)


async def _load_settings_into_cache():
    async with AsyncSessionLocal() as session:
        svc = SettingService(session)
        items = await svc.get_all_settings()
        cache = {item.key: item.value for item in items}
        app.state.settings_cache = cache


@app.on_event("startup")
async def startup_load_settings():
    # Load settings into memory cache at startup
    try:
        await _load_settings_into_cache()
    except Exception:
        # don't crash the app if DB unavailable at startup; initialize empty cache
        app.state.settings_cache = {}

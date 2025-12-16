from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Any, Optional
import cloudinary
import cloudinary.uploader
from app.core.config import settings

router = APIRouter()


def _configure_cloudinary():
    # Configure cloudinary from environment variables (.env already loaded by pydantic-settings)
    # Prefer values from the pydantic Settings object (reads .env)
    cloudinary.config(
        cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET,
        secure=True,
    )


@router.post("/image", tags=["uploads"])
async def upload_image(file: UploadFile = File(...)) -> Any:
    """Public endpoint to upload an image to Cloudinary. No auth required.

    Returns Cloudinary upload result (url, public_id, etc.).
    """
    _configure_cloudinary()

    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image uploads are allowed")

    try:
        # cloudinary.uploader.upload accepts file-like objects; UploadFile.file is suitable
        # Ensure file pointer is at start (some clients may have consumed it)
        try:
            file.file.seek(0)
        except Exception:
            pass

        result = cloudinary.uploader.upload(file.file, resource_type="image")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Upload failed: {exc}")

    return {"url": result.get("secure_url") or result.get("url"), "public_id": result.get("public_id"), "raw": result}


@router.delete("/image", tags=["uploads"])
async def delete_image(public_id: Optional[str] = None, url: Optional[str] = None) -> Any:
    """Delete an image from Cloudinary by `public_id` or by full `url`.

    Examples:
    - DELETE /api/v1/uploads/image?public_id=abc123
    - DELETE /api/v1/uploads/image?url=https://res.cloudinary.com/.../v123/.../abc123.jpg
    """
    _configure_cloudinary()

    if not public_id and not url:
        raise HTTPException(status_code=400, detail="Provide either `public_id` or `url` to delete")

    if not public_id and url:
        # try to extract public_id from URL (take last path segment, strip extension)
        try:
            last_segment = url.rstrip("/\n").rsplit("/", 1)[-1]
            public_id = last_segment.split(".", 1)[0]
        except Exception:
            raise HTTPException(status_code=400, detail="Could not extract public_id from url")

    try:
        result = cloudinary.uploader.destroy(public_id, resource_type="image", invalidate=True)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Delete failed: {exc}")

    return {"public_id": public_id, "raw": result}

from fastapi import APIRouter
from . import students_router
from . import groups_router
from . import attendance_router
from . import subjects_router
from . import rooms_router
from . import verifications_router
from . import sessions_router
from . import course_offerings_router


# Mount the main Student routes
router = APIRouter()
router.include_router(students_router.router, prefix="/students")
router.include_router(groups_router.router, prefix="/groups")
router.include_router(attendance_router.router, prefix="/attendance")
router.include_router(subjects_router.router, prefix="/subjects")
router.include_router(rooms_router.router, prefix="/rooms")
router.include_router(verifications_router.router, prefix="/verifications")
router.include_router(sessions_router.router, prefix="/sessions")
router.include_router(course_offerings_router.router, prefix="/course_offerings")
from fastapi import APIRouter

from . import lecturers_router
from . import rooms_router
from . import departments_router
from . import generations_router
from . import groups_router
from . import specializations_router
from . import terms_router
from . import sessions_router
from . import attendance_router
from . import students_router
from . import subjects_router
from . import verifications_router
from . import course_offerings_router

# Composite users router to mirror the lecturers layout
router = APIRouter()


# Mount the main lecturer routes (lecturers_router defines routes like `/`, `/{id}`, etc.)
router.include_router(lecturers_router.router, prefix="/lecturers")

# Mount nested lecturer areas under clear prefixes
router.include_router(rooms_router.router, prefix="/rooms")
router.include_router(departments_router.router, prefix="/departments")
router.include_router(generations_router.router, prefix="/generations")
router.include_router(groups_router.router, prefix="/groups")
router.include_router(specializations_router.router, prefix="/specializations")
router.include_router(terms_router.router, prefix="/terms")
router.include_router(sessions_router.router, prefix="/sessions")
router.include_router(attendance_router.router, prefix="/attendance")
router.include_router(students_router.router, prefix="/students")
router.include_router(subjects_router.router, prefix="/subjects")
router.include_router(verifications_router.router, prefix="/verifications")
router.include_router(course_offerings_router.router, prefix="/course_offerings")
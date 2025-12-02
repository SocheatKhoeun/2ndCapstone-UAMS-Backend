from fastapi import APIRouter

from app.api.v1.admins import subjects_router

from . import instructors_router
from . import settings_router
from . import admins_router
from . import students_router
from . import generations_router
from . import departments_router
from . import specializations_router
from . import terms_router
from . import groups_router
from . import rooms_router
from . import course_offerings_router
from . import enrollments_router
from . import sessions_router
from . import biometric_templates_router
from . import verifications_router
from . import attendance_router

# Composite admin router which groups admin-related sub-routers.
# This module should only expose an APIRouter instance named `router` so
# the top-level `app.api.v1.router` can mount it once with the 
# desired `/admins` prefix.
router = APIRouter()

# Mount the main admins routes (admins_router defines routes like `/`, `/{id}`, etc.)
router.include_router(admins_router.router, prefix="/admins")

# Mount nested admin areas under clear prefixes
router.include_router(instructors_router.router, prefix="/instructors")
router.include_router(students_router.router, prefix="/students")
router.include_router(generations_router.router, prefix="/generations")
router.include_router(settings_router.router, prefix="/settings")
router.include_router(departments_router.router, prefix="/departments")
router.include_router(specializations_router.router, prefix="/specializations")
router.include_router(subjects_router.router, prefix="/subjects")
router.include_router(terms_router.router, prefix="/terms")
router.include_router(groups_router.router, prefix="/groups")
router.include_router(rooms_router.router, prefix="/rooms")
router.include_router(course_offerings_router.router, prefix="/course_offerings")
router.include_router(enrollments_router.router, prefix="/enrollments")
router.include_router(sessions_router.router, prefix="/sessions")
router.include_router(biometric_templates_router.router, prefix="/biometric_templates")
router.include_router(verifications_router.router, prefix="/verifications")
router.include_router(attendance_router.router, prefix="/attendance")

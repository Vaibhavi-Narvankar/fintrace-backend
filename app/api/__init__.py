from fastapi import APIRouter
from .user import router as user_router
from .expense import router as expense_router
from .category import router as category_router
from .profile import router as profile_router
from .dashboard import router as dashboard_router

router = APIRouter()
router.include_router(user_router)
router.include_router(expense_router)
router.include_router(category_router)
router.include_router(profile_router)
router.include_router(dashboard_router)
from fastapi import APIRouter

from .products.views import router as product_router
from .users.views import router as users_router
from .demo_auth.views import router as demo_auth_router

router = APIRouter(
    prefix="/api/v1",
)

router.include_router(product_router)
router.include_router(users_router)
router.include_router(demo_auth_router)

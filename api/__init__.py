from fastapi import APIRouter
from .floor_plan import router as img_operations_router

router = APIRouter()

router.include_router(img_operations_router)


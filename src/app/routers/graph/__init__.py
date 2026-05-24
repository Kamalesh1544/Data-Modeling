from __future__ import annotations

from fastapi import APIRouter

from .category import router as category_router
from .customer import router as customer_router
from .init_db import router as init_router
from .product import router as product_router


def get_router() -> APIRouter:
    router = APIRouter(prefix="/api/graph")
    router.include_router(init_router)
    router.include_router(customer_router)
    router.include_router(product_router)
    router.include_router(category_router)
    return router


__all__ = ["get_router"]

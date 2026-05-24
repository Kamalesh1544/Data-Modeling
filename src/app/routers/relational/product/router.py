from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from injectq.integrations.fastapi import InjectFastAPI

from src.app.core.auth import get_current_user
from src.app.routers.relational.product.schemas.product_schema import (
    ProductRecommendationResponse,
    TopProductResponse,
)
from src.app.routers.relational.product.services.product_service import (
    ProductService,
)
from src.app.utils.schemas import AuthUserSchema


router = APIRouter(tags=["PostgreSQL — Products"])


@router.get("/top-products")
async def top_products(
    user: AuthUserSchema = Depends(get_current_user),
    limit: int = Query(5, ge=1, le=50),
    service: Annotated[ProductService, InjectFastAPI(ProductService)] = None,  # type: ignore[assignment]
) -> list[TopProductResponse]:
    results = await service.get_top_products(limit)
    return [TopProductResponse(**r) for r in results]


@router.get("/recommendations/{product_id}")
async def product_recommendations(
    product_id: int,
    user: AuthUserSchema = Depends(get_current_user),
    limit: int = Query(5, ge=1, le=20),
    service: Annotated[ProductService, InjectFastAPI(ProductService)] = None,  # type: ignore[assignment]
) -> list[ProductRecommendationResponse]:
    results = await service.get_product_recommendations(product_id, limit)
    return [ProductRecommendationResponse(**r) for r in results]


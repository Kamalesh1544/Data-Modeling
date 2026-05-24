from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from injectq.integrations.fastapi import InjectFastAPI

from src.app.core.auth import get_current_user
from src.app.routers.graph.product.schemas.product_schema import (
    RecommendationResponse,
    TopProductResponse,
)
from src.app.routers.graph.product.services.product_service import (
    ProductService,
)
from src.app.utils.schemas import AuthUserSchema


router = APIRouter(tags=["Neo4j — Products"])


@router.get("/recommendations/{product_name}")
async def also_bought(
    product_name: str,
    user: AuthUserSchema = Depends(get_current_user),
    limit: int = Query(5, ge=1, le=20),
    service: Annotated[ProductService, InjectFastAPI(ProductService)] = None,  # type: ignore[assignment]
) -> list[RecommendationResponse]:
    results = await service.get_also_bought_recommendations(product_name, limit)
    return [RecommendationResponse(**r) for r in results]


@router.get("/top-products")
async def top_products(
    user: AuthUserSchema = Depends(get_current_user),
    limit: int = Query(5, ge=1, le=20),
    service: Annotated[ProductService, InjectFastAPI(ProductService)] = None,  # type: ignore[assignment]
) -> list[TopProductResponse]:
    results = await service.get_top_products(limit)
    return [TopProductResponse(**r) for r in results]


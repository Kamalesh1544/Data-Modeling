from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from injectq.integrations.fastapi import InjectFastAPI

from src.app.core.auth import get_current_user
from src.app.routers.graph.category.schemas.category_schema import (
    CategoryProductResponse,
)
from src.app.routers.graph.category.services.category_service import (
    CategoryService,
)
from src.app.utils.schemas import AuthUserSchema


router = APIRouter(tags=["Neo4j — Categories"])


@router.get("/category-products/{category}")
async def category_products(
    category: str,
    user: AuthUserSchema = Depends(get_current_user),
    service: Annotated[CategoryService, InjectFastAPI(CategoryService)] = None,  # type: ignore[assignment]
) -> list[CategoryProductResponse]:
    results = await service.get_products_by_category(category)
    return [CategoryProductResponse(**r) for r in results]


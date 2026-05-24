from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from injectq.integrations.fastapi import InjectFastAPI

from src.app.core.auth import get_current_user
from src.app.routers.document.product.schemas.product_schema import (
    ProductDocumentResponse,
)
from src.app.routers.document.product.services.product_service import (
    ProductService,
)
from src.app.utils.schemas import AuthUserSchema


router = APIRouter(tags=["MongoDB — Products"])


@router.get("/products/{category}")
async def products_by_category(
    category: str,
    user: AuthUserSchema = Depends(get_current_user),
    service: Annotated[ProductService, InjectFastAPI(ProductService)] = None,  # type: ignore[assignment]
) -> list[ProductDocumentResponse]:
    results = await service.get_products_by_category(category)
    return [ProductDocumentResponse(**r) for r in results]


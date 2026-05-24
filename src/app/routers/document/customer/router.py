from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from injectq.integrations.fastapi import InjectFastAPI

from src.app.core.auth import get_current_user
from src.app.routers.document.customer.schemas.customer_schema import (
    CustomerDocumentResponse,
)
from src.app.routers.document.customer.services.customer_service import (
    CustomerService,
)
from src.app.utils.schemas import AuthUserSchema


router = APIRouter(tags=["MongoDB — Customers"])


@router.get("/customers")
async def customers(
    user: AuthUserSchema = Depends(get_current_user),
    limit: int = Query(10, ge=1, le=100),
    service: Annotated[CustomerService, InjectFastAPI(CustomerService)] = None,  # type: ignore[assignment]
) -> list[CustomerDocumentResponse]:
    results = await service.get_customers_with_embeddings(limit)
    return [CustomerDocumentResponse(**r) for r in results]


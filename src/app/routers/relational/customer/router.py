from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from injectq.integrations.fastapi import InjectFastAPI

from src.app.core.auth import get_current_user
from src.app.routers.relational.customer.schemas.customer_schema import (
    CustomerPurchaseResponse,
)
from src.app.routers.relational.customer.services.customer_service import (
    CustomerService,
)
from src.app.utils.schemas import AuthUserSchema


router = APIRouter(tags=["PostgreSQL — Customers"])


@router.get("/customers-with-purchases")
async def customers_with_purchases(
    user: AuthUserSchema = Depends(get_current_user),
    limit: int = Query(10, ge=1, le=100),
    service: Annotated[CustomerService, InjectFastAPI(CustomerService)] = None,  # type: ignore[assignment]
) -> list[CustomerPurchaseResponse]:
    results = await service.get_customers_with_purchases(limit)
    return [CustomerPurchaseResponse(**r) for r in results]


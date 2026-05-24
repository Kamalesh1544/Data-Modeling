from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from injectq.integrations.fastapi import InjectFastAPI

from src.app.core.auth import get_current_user
from src.app.routers.graph.customer.schemas.customer_schema import (
    PurchaseHistoryResponse,
)
from src.app.routers.graph.customer.services.customer_service import (
    CustomerService,
)
from src.app.utils.schemas import AuthUserSchema


router = APIRouter(tags=["Neo4j — Customers"])


@router.get("/customer-history/{customer_email}")
async def purchase_history(
    customer_email: str,
    user: AuthUserSchema = Depends(get_current_user),
    service: Annotated[CustomerService, InjectFastAPI(CustomerService)] = None,  # type: ignore[assignment]
) -> list[PurchaseHistoryResponse]:
    results = await service.get_purchase_history(customer_email)
    return [PurchaseHistoryResponse(**r) for r in results]


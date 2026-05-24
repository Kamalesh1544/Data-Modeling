from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from injectq.integrations.fastapi import InjectFastAPI

from src.app.core.auth import get_current_user
from src.app.routers.document.purchase.schemas.purchase_schema import (
    PurchaseDocumentResponse,
)
from src.app.routers.document.purchase.services.purchase_service import (
    PurchaseService,
)
from src.app.utils.schemas import AuthUserSchema


router = APIRouter(tags=["MongoDB — Purchases"])


@router.get("/purchases/{customer_email}")
async def purchases_by_customer(
    customer_email: str,
    user: AuthUserSchema = Depends(get_current_user),
    service: Annotated[PurchaseService, InjectFastAPI(PurchaseService)] = None,  # type: ignore[assignment]
) -> list[PurchaseDocumentResponse]:
    results = await service.get_purchases_by_customer(customer_email)
    return [PurchaseDocumentResponse(**r) for r in results]


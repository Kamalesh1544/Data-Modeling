from __future__ import annotations

from pydantic import BaseModel


class PurchaseHistoryResponse(BaseModel):
    product_name: str
    category: str | None = None
    amount: float | None = None
    purchase_date: str | None = None
    quantity: int | None = None

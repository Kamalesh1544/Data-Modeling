from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class PurchaseDocumentResponse(BaseModel):
    id: str
    customer_id: str
    product_id: str
    quantity: int
    total_amount: float
    purchase_date: datetime
    payment_method: str | None = None

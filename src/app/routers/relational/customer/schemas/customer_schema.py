from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class CustomerPurchaseResponse(BaseModel):
    customer_id: int
    first_name: str
    last_name: str
    email: str
    industry: str | None = None
    purchase_id: int | None = None
    product_id: int | None = None
    product_name: str | None = None
    quantity: int | None = None
    total_amount: Decimal | None = None
    purchase_date: datetime | None = None

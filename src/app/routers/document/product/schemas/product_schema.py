from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class ProductDocumentResponse(BaseModel):
    id: str
    name: str
    category: str
    unit_price: float
    description: str | None = None
    stock_quantity: int | None = None
    created_at: datetime | None = None

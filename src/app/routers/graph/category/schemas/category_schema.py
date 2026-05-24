from __future__ import annotations

from pydantic import BaseModel


class CategoryProductResponse(BaseModel):
    product_name: str
    unit_price: float | None = None
    product_id: int | None = None

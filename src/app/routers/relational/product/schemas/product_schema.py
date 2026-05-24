from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel


class TopProductResponse(BaseModel):
    product_id: int
    name: str
    category: str | None = None
    unit_price: Decimal | None = None
    total_sold: int = 0
    avg_rating: Decimal | None = None


class ProductRecommendationResponse(BaseModel):
    product_id: int
    name: str
    category: str | None = None
    unit_price: Decimal | None = None
    times_bought_together: int = 0


class InitResponse(BaseModel):
    message: str
    tables_seeded: dict[str, int]

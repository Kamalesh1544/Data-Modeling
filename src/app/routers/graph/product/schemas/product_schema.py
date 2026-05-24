from __future__ import annotations

from pydantic import BaseModel


class RecommendationResponse(BaseModel):
    product_name: str
    category: str | None = None
    unit_price: float | None = None
    recommendation_score: int | None = None


class TopProductResponse(BaseModel):
    product_name: str
    category: str | None = None
    purchase_count: int = 0
    total_revenue: float | None = None

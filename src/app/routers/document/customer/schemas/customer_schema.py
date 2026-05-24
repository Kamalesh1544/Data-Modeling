from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class PurchaseEmbedding(BaseModel):
    product_id: str
    product_name: str
    amount: float
    date: datetime


class MatchedProduct(BaseModel):
    product_id: str
    product_name: str
    reason: str


class CustomerDocumentResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    industry: str | None = None
    recent_purchases: list[PurchaseEmbedding] = []
    matched_products: list[MatchedProduct] = []
    created_at: datetime | None = None

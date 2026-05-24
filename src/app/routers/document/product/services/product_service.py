from __future__ import annotations

from typing import Any

from injectq import inject, singleton
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from src.app.routers.document.product.repositories.product_repo import (
    ProductRepo,
)


DEFAULT_URI = "mongodb://localhost:27017"
DEFAULT_DB = "ecommerce_nosql"


@singleton
class ProductService:
    @inject
    def __init__(self, product_repo: ProductRepo) -> None:
        self._repo = product_repo

    async def get_products_by_category(
        self, category: str
    ) -> list[dict[str, Any]]:
        client = AsyncIOMotorClient(DEFAULT_URI)
        try:
            db: AsyncIOMotorDatabase = client[DEFAULT_DB]
            return await self._repo.get_products_by_category(db, category)
        finally:
            client.close()


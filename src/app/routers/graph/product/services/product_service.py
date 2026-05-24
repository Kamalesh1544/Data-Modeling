from __future__ import annotations

from typing import Any

from injectq import inject, singleton
from neo4j import AsyncGraphDatabase

from src.app.routers.graph.product.repositories.product_repo import (
    ProductRepo,
)


DEFAULT_URI = "bolt://localhost:7687"
DEFAULT_USER = "neo4j"
DEFAULT_PASSWORD = "password"  # noqa: S105


@singleton
class ProductService:
    @inject
    def __init__(self, product_repo: ProductRepo) -> None:
        self._repo = product_repo

    async def get_also_bought_recommendations(
        self, product_name: str, limit: int = 5
    ) -> list[dict[str, Any]]:
        driver = AsyncGraphDatabase.driver(
            DEFAULT_URI,
            auth=(DEFAULT_USER, DEFAULT_PASSWORD),
        )
        async with driver:
            return await self._repo.get_also_bought_recommendations(
                driver, product_name, limit
            )

    async def get_top_products(self, limit: int = 5) -> list[dict[str, Any]]:
        driver = AsyncGraphDatabase.driver(
            DEFAULT_URI,
            auth=(DEFAULT_USER, DEFAULT_PASSWORD),
        )
        async with driver:
            return await self._repo.get_top_products(driver, limit)


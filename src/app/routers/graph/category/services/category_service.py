from __future__ import annotations

from typing import Any

from injectq import inject, singleton
from neo4j import AsyncGraphDatabase

from src.app.routers.graph.category.repositories.category_repo import (
    CategoryRepo,
)


DEFAULT_URI = "bolt://localhost:7687"
DEFAULT_USER = "neo4j"
DEFAULT_PASSWORD = "password"  # noqa: S105


@singleton
class CategoryService:
    @inject
    def __init__(self, category_repo: CategoryRepo) -> None:
        self._repo = category_repo

    async def get_products_by_category(
        self, category: str
    ) -> list[dict[str, Any]]:
        driver = AsyncGraphDatabase.driver(
            DEFAULT_URI,
            auth=(DEFAULT_USER, DEFAULT_PASSWORD),
        )
        async with driver:
            return await self._repo.get_products_by_category(driver, category)


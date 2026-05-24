from __future__ import annotations

from typing import Any

from injectq import inject, singleton
from neo4j import AsyncGraphDatabase

from src.app.routers.graph.customer.repositories.customer_repo import (
    CustomerRepo,
)


DEFAULT_URI = "bolt://localhost:7687"
DEFAULT_USER = "neo4j"
DEFAULT_PASSWORD = "password"  # noqa: S105


@singleton
class CustomerService:
    @inject
    def __init__(self, customer_repo: CustomerRepo) -> None:
        self._repo = customer_repo

    async def get_purchase_history(
        self, customer_email: str
    ) -> list[dict[str, Any]]:
        driver = AsyncGraphDatabase.driver(
            DEFAULT_URI,
            auth=(DEFAULT_USER, DEFAULT_PASSWORD),
        )
        async with driver:
            return await self._repo.get_purchase_history(driver, customer_email)


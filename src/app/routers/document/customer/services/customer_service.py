from __future__ import annotations

from typing import Any

from injectq import inject, singleton
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from src.app.routers.document.customer.repositories.customer_repo import (
    CustomerRepo,
)


DEFAULT_URI = "mongodb://localhost:27017"
DEFAULT_DB = "ecommerce_nosql"


@singleton
class CustomerService:
    @inject
    def __init__(self, customer_repo: CustomerRepo) -> None:
        self._repo = customer_repo

    async def get_customers_with_embeddings(
        self, limit: int = 10
    ) -> list[dict[str, Any]]:
        client = AsyncIOMotorClient(DEFAULT_URI)
        try:
            db: AsyncIOMotorDatabase = client[DEFAULT_DB]
            return await self._repo.get_customers_with_embeddings(db, limit)
        finally:
            client.close()


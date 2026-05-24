from __future__ import annotations

from typing import Any

from injectq import inject, singleton
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from src.app.routers.document.purchase.repositories.purchase_repo import (
    PurchaseRepo,
)


DEFAULT_URI = "mongodb://localhost:27017"
DEFAULT_DB = "ecommerce_nosql"


@singleton
class PurchaseService:
    @inject
    def __init__(self, purchase_repo: PurchaseRepo) -> None:
        self._repo = purchase_repo

    async def get_purchases_by_customer(
        self, customer_email: str
    ) -> list[dict[str, Any]]:
        client = AsyncIOMotorClient(DEFAULT_URI)
        try:
            db: AsyncIOMotorDatabase = client[DEFAULT_DB]
            return await self._repo.get_purchases_by_customer(
                db, customer_email
            )
        finally:
            client.close()


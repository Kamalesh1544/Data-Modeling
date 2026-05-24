from __future__ import annotations

from injectq import singleton
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.app.core import logger


@singleton
class InitDBRepo:
    async def init_collections(
        self, db: AsyncIOMotorDatabase
    ) -> None:
        existing = await db.list_collection_names()
        for name in ("customers", "products", "purchases"):
            if name not in existing:
                await db.create_collection(name)
                logger.info("Created MongoDB collection: %s", name)

    async def seed_all(
        self,
        db: AsyncIOMotorDatabase,
        product_ids: list[str],
        customer_ids: list[str],
        purchase_ids: list[str],
    ) -> dict[str, int]:
        return {
            "products": len(product_ids),
            "customers": len(customer_ids),
            "purchases": len(purchase_ids),
        }

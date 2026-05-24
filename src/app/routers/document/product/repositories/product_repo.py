from __future__ import annotations

from typing import Any

from injectq import singleton
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.app.core import logger


@singleton
class ProductRepo:
    async def seed_products(
        self, db: AsyncIOMotorDatabase, products: list[dict[str, Any]]
    ) -> list[str]:
        result = await db["products"].insert_many(products)
        ids = [str(oid) for oid in result.inserted_ids]
        logger.info("Inserted %d products into MongoDB", len(ids))
        return ids

    async def get_products_by_category(
        self,
        db: AsyncIOMotorDatabase,
        category: str,
    ) -> list[dict[str, Any]]:
        cursor = db["products"].find({"category": category})
        return [self._serialize_doc(doc) async for doc in cursor]

    def _serialize_doc(self, doc: Any) -> dict[str, Any]:
        doc["id"] = str(doc.pop("_id"))
        return doc

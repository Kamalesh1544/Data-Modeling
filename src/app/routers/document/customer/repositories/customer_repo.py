from __future__ import annotations

from typing import Any

from injectq import singleton
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.app.core import logger


@singleton
class CustomerRepo:
    async def seed_customers_with_embeddings(
        self,
        db: AsyncIOMotorDatabase,
        customers: list[dict[str, Any]],
    ) -> list[str]:
        result = await db["customers"].insert_many(customers)
        ids = [str(oid) for oid in result.inserted_ids]
        logger.info("Inserted %d customers with embedded documents", len(ids))
        return ids

    async def get_customers_with_embeddings(
        self,
        db: AsyncIOMotorDatabase,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        cursor = db["customers"].find().limit(limit)
        return [self._serialize_doc(doc) async for doc in cursor]

    def _serialize_doc(self, doc: Any) -> dict[str, Any]:
        doc["id"] = str(doc.pop("_id"))
        return doc

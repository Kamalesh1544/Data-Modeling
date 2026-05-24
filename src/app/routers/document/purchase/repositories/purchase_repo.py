from __future__ import annotations

from typing import Any

from injectq import singleton
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.app.core import logger


@singleton
class PurchaseRepo:
    async def seed_purchases_with_refs(
        self,
        db: AsyncIOMotorDatabase,
        purchases: list[dict[str, Any]],
    ) -> list[str]:
        result = await db["purchases"].insert_many(purchases)
        ids = [str(oid) for oid in result.inserted_ids]
        logger.info("Inserted %d purchases with referencing", len(ids))
        return ids

    async def get_purchases_by_customer(
        self,
        db: AsyncIOMotorDatabase,
        customer_email: str,
    ) -> list[dict[str, Any]]:
        customer = await db["customers"].find_one({"email": customer_email})
        if not customer:
            return []
        cursor = db["purchases"].find({"customer_id": str(customer["_id"])})
        return [self._serialize_doc(doc) async for doc in cursor]

    def _serialize_doc(self, doc: Any) -> dict[str, Any]:
        doc["id"] = str(doc.pop("_id"))
        return doc

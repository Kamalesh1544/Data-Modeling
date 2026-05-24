from __future__ import annotations

from typing import Any

from injectq import inject, singleton
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from src.app.routers.document.customer.repositories.customer_repo import (
    CustomerRepo,
)
from src.app.routers.document.init_db.repositories.init_db_repo import (
    InitDBRepo,
)
from src.app.routers.document.product.repositories.product_repo import (
    ProductRepo,
)
from src.app.routers.document.purchase.repositories.purchase_repo import (
    PurchaseRepo,
)


DEFAULT_URI = "mongodb://localhost:27017"
DEFAULT_DB = "ecommerce_nosql"


@singleton
class InitDBService:
    @inject
    def __init__(
        self,
        init_db_repo: InitDBRepo,
        product_repo: ProductRepo,
        customer_repo: CustomerRepo,
        purchase_repo: PurchaseRepo,
    ) -> None:
        self._init_repo = init_db_repo
        self._product_repo = product_repo
        self._customer_repo = customer_repo
        self._purchase_repo = purchase_repo

    async def init_database(
        self,
        products: list[dict[str, Any]] | None = None,
        customers: list[dict[str, Any]] | None = None,
        purchases: list[dict[str, Any]] | None = None,
    ) -> dict[str, int]:
        client = AsyncIOMotorClient(DEFAULT_URI)
        try:
            db: AsyncIOMotorDatabase = client[DEFAULT_DB]
            await self._init_repo.init_collections(db)
            product_ids = (
                await self._product_repo.seed_products(db, products)
                if products else []
            )
            customer_ids = (
                await self._customer_repo.seed_customers_with_embeddings(db, customers)
                if customers else []
            )
            purchase_ids = (
                await self._purchase_repo.seed_purchases_with_refs(db, purchases)
                if purchases else []
            )
            return await self._init_repo.seed_all(
                db, product_ids, customer_ids, purchase_ids
            )
        finally:
            client.close()


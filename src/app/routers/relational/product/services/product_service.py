from __future__ import annotations

from typing import Any

import asyncpg
from injectq import inject, singleton

from src.app.core.config.settings import get_settings
from src.app.routers.relational.product.repositories.product_repo import (
    ProductRepo,
)


@singleton
class ProductService:
    @inject
    def __init__(self, product_repo: ProductRepo) -> None:
        self._repo = product_repo

    async def get_top_products(self, limit: int = 5) -> list[dict[str, Any]]:
        conn = await _get_connection()
        try:
            return await self._repo.fetch_top_products(conn, limit)
        finally:
            await conn.close()

    async def get_product_recommendations(
        self, product_id: int, limit: int = 5
    ) -> list[dict[str, Any]]:
        conn = await _get_connection()
        try:
            return await self._repo.fetch_product_recommendations(
                conn, product_id, limit
            )
        finally:
            await conn.close()


def _build_dsn() -> str:
    s = get_settings()
    return (
        f"postgresql://{s.POSTGRES_USER}:{s.POSTGRES_PASSWORD}"
        f"@{s.POSTGRES_HOST}:{s.POSTGRES_PORT}/{s.POSTGRES_DB}"
    )


async def _get_connection(dsn: str | None = None) -> asyncpg.Connection:
    return await asyncpg.connect(dsn or _build_dsn())


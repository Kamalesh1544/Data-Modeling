from __future__ import annotations

from typing import Any

import asyncpg
from injectq import inject, singleton

from src.app.core.config.settings import get_settings
from src.app.routers.relational.customer.repositories.customer_repo import (
    CustomerRepo,
)


@singleton
class CustomerService:
    @inject
    def __init__(self, customer_repo: CustomerRepo) -> None:
        self._repo = customer_repo

    async def get_customers_with_purchases(
        self, limit: int = 10
    ) -> list[dict[str, Any]]:
        conn = await _get_connection()
        try:
            return await self._repo.fetch_customers_with_purchases(conn, limit)
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


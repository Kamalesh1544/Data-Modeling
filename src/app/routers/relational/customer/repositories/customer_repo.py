from __future__ import annotations

from typing import Any

import asyncpg
from injectq import singleton


@singleton
class CustomerRepo:
    async def fetch_customers_with_purchases(
        self,
        conn: asyncpg.Connection,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        rows = await conn.fetch(
            """
            SELECT
                c.customer_id, c.first_name, c.last_name, c.email, c.industry,
                p.purchase_id, p.product_id, pr.name AS product_name,
                p.quantity, p.total_amount, p.purchase_date
            FROM customers c
            LEFT JOIN purchases p ON c.customer_id = p.customer_id
            LEFT JOIN products pr ON p.product_id = pr.product_id
            ORDER BY c.customer_id, p.purchase_date DESC
            LIMIT $1
            """,
            limit,
        )
        return [dict(r) for r in rows]

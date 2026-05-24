from __future__ import annotations

from typing import Any

import asyncpg
from injectq import singleton


@singleton
class ProductRepo:
    async def fetch_top_products(
        self,
        conn: asyncpg.Connection,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        rows = await conn.fetch(
            """
            SELECT
                pr.product_id, pr.name, pr.category, pr.unit_price,
                COALESCE(SUM(p.quantity), 0) AS total_sold,
                COALESCE(AVG(ur.rating), 0)::NUMERIC(3,2) AS avg_rating
            FROM products pr
            LEFT JOIN purchases p ON pr.product_id = p.product_id
            LEFT JOIN user_ratings ur ON pr.product_id = ur.product_id
            GROUP BY pr.product_id
            ORDER BY total_sold DESC
            LIMIT $1
            """,
            limit,
        )
        return [dict(r) for r in rows]

    async def fetch_product_recommendations(
        self,
        conn: asyncpg.Connection,
        product_id: int,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        rows = await conn.fetch(
            """
            WITH buyers AS (
                SELECT DISTINCT customer_id FROM purchases WHERE product_id = $1
            )
            SELECT
                pr.product_id, pr.name, pr.category, pr.unit_price,
                COUNT(*) AS times_bought_together
            FROM purchases p
            JOIN products pr ON p.product_id = pr.product_id
            WHERE p.customer_id IN (SELECT customer_id FROM buyers)
              AND p.product_id != $1
            GROUP BY pr.product_id
            ORDER BY times_bought_together DESC
            LIMIT $2
            """,
            product_id,
            limit,
        )
        return [dict(r) for r in rows]

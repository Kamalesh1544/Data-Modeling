from __future__ import annotations

from typing import Any

from injectq import singleton
from neo4j import AsyncDriver


@singleton
class CategoryRepo:
    async def get_products_by_category(
        self,
        driver: AsyncDriver,
        category: str,
    ) -> list[dict[str, Any]]:
        async with driver.session() as session:
            result = await session.run(
                """
                MATCH (p:Product)-[:BELONGS_TO]->(c:Category {name: $category})
                RETURN p.name AS product_name,
                       p.unit_price AS unit_price,
                       p.product_id AS product_id
                ORDER BY p.unit_price ASC
                """,
                category=category,
            )
            return [dict(r) async for r in result]

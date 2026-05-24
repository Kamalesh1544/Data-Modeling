from __future__ import annotations

from typing import Any

from injectq import singleton
from neo4j import AsyncDriver


@singleton
class ProductRepo:
    async def get_also_bought_recommendations(
        self,
        driver: AsyncDriver,
        product_name: str,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        async with driver.session() as session:
            result = await session.run(
                """
                MATCH (p1:Product {name: $product_name})<-[:PURCHASED]-()-[*..2]-(other:Product)
                WHERE other <> p1
                RETURN DISTINCT other.name AS product_name,
                       other.category AS category,
                       other.unit_price AS unit_price,
                       COUNT(*) AS recommendation_score
                ORDER BY recommendation_score DESC
                LIMIT $limit
                """,
                product_name=product_name,
                limit=limit,
            )
            return [dict(r) async for r in result]

    async def get_top_products(
        self,
        driver: AsyncDriver,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        async with driver.session() as session:
            result = await session.run(
                """
                MATCH (c:Customer)-[p:PURCHASED]->(prod:Product)
                RETURN prod.name AS product_name,
                       prod.category AS category,
                       COUNT(*) AS purchase_count,
                       SUM(p.amount) AS total_revenue
                ORDER BY purchase_count DESC
                LIMIT $limit
                """,
                limit=limit,
            )
            return [dict(r) async for r in result]

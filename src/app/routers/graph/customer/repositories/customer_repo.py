from __future__ import annotations

from typing import Any

from injectq import singleton
from neo4j import AsyncDriver


@singleton
class CustomerRepo:
    async def get_purchase_history(
        self,
        driver: AsyncDriver,
        customer_email: str,
    ) -> list[dict[str, Any]]:
        async with driver.session() as session:
            result = await session.run(
                """
                MATCH (c:Customer {email: $email})-[p:PURCHASED]->(prod:Product)
                RETURN prod.name AS product_name,
                       prod.category AS category,
                       p.amount AS amount,
                       p.date AS purchase_date,
                       p.quantity AS quantity
                ORDER BY p.date DESC
                """,
                email=customer_email,
            )
            return [dict(r) async for r in result]

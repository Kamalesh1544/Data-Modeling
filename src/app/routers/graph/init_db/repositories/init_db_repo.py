from __future__ import annotations

from injectq import singleton
from neo4j import AsyncDriver

from src.app.core import logger


@singleton
class InitDBRepo:
    async def create_graph_schema(
        self, driver: AsyncDriver, cypher_statements: list[str] | None = None
    ) -> None:
        async with driver.session() as session:
            await session.run("MATCH (n) DETACH DELETE n")
            for statement in cypher_statements or []:
                await session.run(statement)
            logger.info("Executed %d Cypher statements", len(cypher_statements or []))

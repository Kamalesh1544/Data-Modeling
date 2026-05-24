from __future__ import annotations

from injectq import inject, singleton
from neo4j import AsyncGraphDatabase

from src.app.routers.graph.init_db.repositories.init_db_repo import (
    InitDBRepo,
)


DEFAULT_URI = "bolt://localhost:7687"
DEFAULT_USER = "neo4j"
DEFAULT_PASSWORD = "password"  # noqa: S105


@singleton
class InitDBService:
    @inject
    def __init__(self, init_db_repo: InitDBRepo) -> None:
        self._repo = init_db_repo

    async def init_database(
        self, cypher_statements: list[str] | None = None
    ) -> dict[str, str]:
        driver = AsyncGraphDatabase.driver(
            DEFAULT_URI,
            auth=(DEFAULT_USER, DEFAULT_PASSWORD),
        )
        async with driver:
            await self._repo.create_graph_schema(driver, cypher_statements)
        return {"status": "created"}


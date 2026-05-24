from __future__ import annotations

import asyncpg
from injectq import inject, singleton

from src.app.core.config.settings import get_settings
from src.app.routers.relational.init_db.repositories.init_db_repo import (
    InitDBRepo,
)


@singleton
class InitDBService:
    @inject
    def __init__(self, init_db_repo: InitDBRepo) -> None:
        self._repo = init_db_repo

    async def init_database(self) -> dict[str, int]:
        conn = await _get_connection()
        try:
            await self._repo.execute_ddl(conn)
            return await self._repo.seed_all(conn)
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


from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import asyncpg
from injectq import singleton

from src.app.core import logger


SEED_DIR = (
    Path(__file__).resolve().parent.parent.parent.parent.parent.parent.parent
    / "db"
    / "seed_data"
)
DDL_PATH = (
    Path(__file__).resolve().parent.parent.parent.parent.parent.parent.parent
    / "db"
    / "relational"
    / "ddl.sql"
)


@dataclass
class _TableInfo:
    name: str
    csv_file: str
    columns: list[str] = field(default_factory=list)


_TABLES = [
    _TableInfo(name="customers", csv_file="customers.csv"),
    _TableInfo(name="products", csv_file="products.csv"),
    _TableInfo(name="purchases", csv_file="purchases.csv"),
    _TableInfo(name="user_ratings", csv_file="user_ratings.csv"),
]


@singleton
class InitDBRepo:
    async def execute_ddl(self, conn: asyncpg.Connection) -> None:
        ddl_sql = DDL_PATH.read_text(encoding="utf-8")
        await conn.execute(ddl_sql)
        logger.info("DDL executed successfully — all 4 tables created.")

    async def _seed_from_csv(
        self, conn: asyncpg.Connection, table: _TableInfo
    ) -> int:
        csv_path = SEED_DIR / table.csv_file
        if not csv_path.exists():
            logger.warning("CSV not found: %s — skipping %s", csv_path, table.name)
            return 0

        with csv_path.open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            if not rows:
                logger.warning("Empty CSV: %s", csv_path)
                return 0

            table.columns = list(rows[0].keys())
            placeholders = ", ".join(
                f"${i + 1}" for i in range(len(table.columns))
            )
            columns = ", ".join(table.columns)

            row_tuples: list[tuple[Any, ...]] = []
            for row in rows:
                row_tuples.append(
                    tuple(row.get(col) for col in table.columns)
                )

            await conn.executemany(
                f"INSERT INTO {table.name} ({columns}) VALUES ({placeholders})",  # noqa: S608
                row_tuples,
            )
            logger.info("Seeded %d rows into %s", len(row_tuples), table.name)
            return len(row_tuples)

    async def seed_all(self, conn: asyncpg.Connection) -> dict[str, int]:
        counts: dict[str, int] = {}
        for table in _TABLES:
            count = await self._seed_from_csv(conn, table)
            counts[table.name] = count
        return counts

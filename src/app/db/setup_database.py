from __future__ import annotations

import asyncio

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from src.app.core import get_settings, logger
from src.app.db.tables.user_constants import USER_TABLES


def get_database_config():
    """
    Generate database configuration based on the DATABASE_TYPE setting.
    Supports both SQLite (for development) and PostgreSQL (for production).

    Returns:
        dict: Database connection configuration for Tortoise ORM
    """
    settings = get_settings()

    if settings.DATABASE_TYPE.lower() == "sqlite":
        logger.info(f"Using SQLite database at: {settings.SQLITE_DB_PATH}")
        return {
            "engine": "tortoise.backends.sqlite",
            "credentials": {
                "file_path": settings.SQLITE_DB_PATH,
            },
        }
    if settings.DATABASE_TYPE.lower() == "postgresql":
        logger.info(
            f"Using PostgreSQL database at: {settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}"
        )
        return {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": settings.POSTGRES_HOST,
                "port": settings.POSTGRES_PORT,
                "user": settings.POSTGRES_USER,
                "password": settings.POSTGRES_PASSWORD,
                "database": settings.POSTGRES_DB,
                "schema": settings.POSTGRES_SCHEMA,
                "minsize": 1,
                "maxsize": 5,
                "max_inactive_connection_lifetime": 300,
                "max_queries": 50000,
            },
        }
    raise ValueError(
        f"Unsupported DATABASE_TYPE: {settings.DATABASE_TYPE}. Use 'sqlite' or 'postgresql'"
    )


TORTOISE_ORM = {
    "connections": {
        "master": get_database_config(),
    },
    "routers": ["src.app.db.router.Router"],
    "apps": {
        "tables": {
            "models": [*USER_TABLES, "aerich.models"],
            "default_connection": "master",
        },
    },
}


async def _init_relational_schema() -> None:
    from src.app.routers.relational.init_db.repositories.init_db_repo import (  # noqa: PLC0415
        InitDBRepo,
    )
    from src.app.routers.relational.init_db.services.init_db_service import (  # noqa: PLC0415
        _get_connection,
    )

    conn = await _get_connection()
    try:
        await InitDBRepo().execute_ddl(conn)
    finally:
        await conn.close()


async def _init_document_schema() -> None:
    from motor.motor_asyncio import AsyncIOMotorClient  # noqa: PLC0415

    from src.app.routers.document.init_db.repositories.init_db_repo import (  # noqa: PLC0415
        InitDBRepo,
    )

    client = AsyncIOMotorClient("mongodb://localhost:27017")
    try:
        db = client["ecommerce_nosql"]
        await InitDBRepo().init_collections(db)
    finally:
        client.close()


def setup_db(app: FastAPI):
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=False,
        add_exception_handlers=False,
    )

    logger.info("Tortoise ORM registered for auth tables")

    asyncio.run(_init_relational_schema())
    logger.info("Relational schema (DDL) ready")

    asyncio.run(_init_document_schema())
    logger.info("Document schema (collections) ready")

    logger.info(
        "Multi-database initialization complete. "
        "Use `python scripts/init_databases.py` to seed data."
    )


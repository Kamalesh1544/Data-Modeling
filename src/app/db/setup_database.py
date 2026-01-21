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
                # choose schema
                "schema": settings.POSTGRES_SCHEMA,
                # Minimum connection pool size
                "minsize": 1,
                # Maximum connection pool size
                "maxsize": 5,
                # Connection timeout
                "max_inactive_connection_lifetime": 300,
                # Maximum number of queries before reconnecting
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


def setup_db(app: FastAPI):
    """
    Set up the database for the FastAPI application using Tortoise ORM.

    This function initializes the Tortoise ORM with the given FastAPI application.
    It registers the Tortoise ORM with the application using the provided configuration.

    Args:
        app (FastAPI): The FastAPI application instance to set up the database for.

    Returns:
        None
    """
    # init tortoise orm
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=False,
        add_exception_handlers=False,
    )

    logger.info("Database setup complete")

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from src.app.core.config.settings import get_settings
from src.app.db.models.user.user_constants import USER_TABLES

TORTOISE_ORM = {
    "connections": {
        "default":
            {
                'engine': 'tortoise.backends.asyncpg',
                'credentials': {
                    'host': get_settings().POSTGRES_HOST,
                    'port': get_settings().POSTGRES_PORT,
                    'user': get_settings().POSTGRES_USER,
                    'password': get_settings().POSTGRES_PASSWORD,
                    'database': get_settings().POSTGRES_DB,
                    'schema': 'cv',  # choose schema
                    'minsize': 1,  # Minimum connection pool size
                    'maxsize': 5,  # Maximum connection pool size
                    'max_inactive_connection_lifetime': 300,  # Connection timeout
                    'max_queries': 50000,  # Maximum number of queries before reconnecting
                }
            },
    },  # postgresql
    # "connections": {"default": "mysql://root:123456@127.0.0.1:3306/test"}, # mysql connections
    # "connections": {"default": "sqlite://:memory:"}, # sqlite in memory database
    # "connections": {"default": "sqlite://./podcast.db"},
    "apps": {
        "models": {
            "models": USER_TABLES + ["aerich.models"],  # For handling migrations],
            "default_connection": "default",
        },
    },
}


def setup_db(app: FastAPI):
    # init tortoise orm
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=False,
        add_exception_handlers=True,
    )

from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from src.app.db.models.user.user_model import UserTable
from src.app.core.config.settings import get_settings
from src.app.db.models.user.user_constants import USER_TABLES


TORTOISE_ORM = {
    "connections": {
        "default": 
        {
            'engine': 'tortoise.backends.asyncpg',
            'credentials': {
                'host':"127.0.0.1", #get_settings().POSTGRES_HOST,
                'port':"5432", #get_settings().POSTGRES_PORT,
                'user':"postgres" ,#get_settings().POSTGRES_USER,
                'password': "123456",#get_settings().POSTGRES_PASSWORD,
                'database':"fastapi",# get_settings().POSTGRES_DB,
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

app = FastAPI()
def setup_db(app: FastAPI):
    # init tortoise orm
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=True,
        add_exception_handlers=True,
    )
    if UserTable.all() is None:
        print("No user found. Creating user")
        

# @app.on_event("startup")
# async def init_db():
#     await Tortoise.init(config=TORTOISE_ORM)
#     await Tortoise.generate_schemas()

# @app.on_event("shutdown")
# async def close_db():   
#     await Tortoise.close_connections()
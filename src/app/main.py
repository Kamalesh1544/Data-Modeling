import logging
from contextlib import asynccontextmanager
from injector import Injector
from fastapi import FastAPI
from tortoise import Tortoise
from fastapi.responses import ORJSONResponse
from fastapi_cache import close_caches
from fastapi_cache.backends.redis import RedisCacheBackend
from starlette.middleware.cors import CORSMiddleware
from fastapi_injector import attach_injector
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from src.app.core.config.settings import get_settings
from src.app.core.config.setup_logs import init_logger
from src.app.core.config.setup_middleware import setup_middleware
from src.app.core.exceptions.handle_errors import init_errors_handler
from src.app.db.setup_database import setup_db
from src.app.routers.setup_router import init_routes


settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the cache
    rc = RedisCacheBackend(settings.REDIS_URL)
    yield
    # Clean up
    await close_caches()
    # close all the connections
    await Tortoise.close_connections()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.MODE == 'DEVELOPMENT',
    summary=settings.SUMMARY,
    docs_url="/docs",
    redoc_url="/redocs",
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)


injector = Injector()
attach_injector(app, injector=injector)

setup_middleware(app)

# setup_db(app)

init_logger(logging.DEBUG)

# init error handler
init_errors_handler(app)

# init routes
init_routes(app)

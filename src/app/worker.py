import os

from fastapi_injector import attach_injector_taskiq
from injector import Injector
from taskiq import (
    InMemoryBroker,
    SimpleRetryMiddleware,
    TaskiqEvents,
    TaskiqState,
)
from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend
from tortoise import Tortoise

from src.app.core.config.settings import get_settings
from src.app.core.config.worker_middleware import MonitoringMiddleware
from src.app.db.setup_database import TORTOISE_ORM
from src.tests.task_tests.setup import register_fake_repos


env = os.environ.get("ENVIRONMENT")
_IS_TEST = env and env == "pytest"

settings = get_settings()

redis_async_result = RedisAsyncResultBackend(
    redis_url=settings.REDIS_URL,
)

# Or you can use PubSubBroker if you need broadcasting
broker = ListQueueBroker(
    url=settings.REDIS_URL,
).with_result_backend(redis_async_result)
broker.add_middlewares(
    [
        MonitoringMiddleware(),
        SimpleRetryMiddleware(default_retry_count=3),
        # PrometheusMiddleware(server_addr="0.0.0.0", server_port=9000),
    ]
)

# this is for testing
if _IS_TEST:
    broker = InMemoryBroker()

# setup injection
injector = Injector()
attach_injector_taskiq(broker.state, injector=injector)
if _IS_TEST:
    register_fake_repos(injector)


@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def startup(state: TaskiqState) -> None:
    if _IS_TEST:
        return
    # Here we store connection pool on startup for later use.
    # state.redis = ConnectionPool.from_url("redis://localhost:6379/1")
    # setup database
    await Tortoise.init(config=TORTOISE_ORM)


@broker.on_event(TaskiqEvents.WORKER_SHUTDOWN)
async def shutdown(state: TaskiqState) -> None:
    if _IS_TEST:
        return
    # Here we close our pool on shutdown event.
    state.redis.disconnect()
    await Tortoise.close_connections()

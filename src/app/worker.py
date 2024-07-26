from uuid import UUID

from fastapi_injector import InjectedTaskiq, attach_injector_taskiq
from injector import Injector
from redis import ConnectionPool
from taskiq import TaskiqEvents, TaskiqState
from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend
from tortoise import Tortoise

from src.app.db.setup_database import TORTOISE_ORM
from src.app.routers.auth.services.user_services import UserService


redis_async_result = RedisAsyncResultBackend(
    redis_url="redis://localhost:6379",
)

# Or you can use PubSubBroker if you need broadcasting
broker = ListQueueBroker(
    url="redis://localhost:6379",
).with_result_backend(redis_async_result)


@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def startup(state: TaskiqState) -> None:
    # Here we store connection pool on startup for later use.
    state.redis = ConnectionPool.from_url("redis://localhost:6379/1")
    # setup database
    await Tortoise.init(config=TORTOISE_ORM)
    # setup injection
    injector = Injector()
    attach_injector_taskiq(state, injector=injector)


@broker.on_event(TaskiqEvents.WORKER_SHUTDOWN)
async def shutdown(state: TaskiqState) -> None:
    # Here we close our pool on shutdown event.
    state.redis.disconnect()
    await Tortoise.close_connections()


@broker.task(task_name="add_task_math2")
async def add_task_math2(x: int, y: int):
    return x + y


# GOAL: get user service it should be injected and then do something
@broker.task(task_name="user_service_post_processing")
async def post_processing_user(
    user_id: int, service: UserService = InjectedTaskiq(UserService)
):
    user = await service.get_user(UUID("2b1e2ae4-ff8a-48f3-8729-be0d754432e9"))
    return user.dict()

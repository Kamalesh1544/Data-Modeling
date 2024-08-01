from uuid import UUID

from fastapi_injector import InjectedTaskiq

from src.app.routers.auth.services.user_services import UserService
from src.app.worker import broker


@broker.task(task_name="add_task_math")
def add_task_math(x: int, y: int):
    return x + y


@broker.task(task_name="user_service_post_processing")
async def post_processing_user(user_id: int, service: UserService = InjectedTaskiq(UserService)):
    user = await service.get_user(UUID("2b1e2ae4-ff8a-48f3-8729-be0d754432e9"))
    return user.dict()

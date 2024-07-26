from uuid import UUID

from fastapi import APIRouter, Depends, Request
from fastapi_injector import Injected

from src.app.core.auth.authentication import get_current_user
from src.app.routers.auth.schemas.user_schemas import UserSchema
from src.app.routers.auth.services.user_services import UserService
from src.app.utils.response_helper import success_response
from src.app.utils.swagger_helper import generate_swagger_responses


router = APIRouter(tags=["User"], dependencies=[Depends(get_current_user)])


@router.get(
    "/v1/users/{user_id}",
    responses=generate_swagger_responses(UserSchema),
    summary="Get user details",
    description="Get user details by user id",
    openapi_extra={},
)
async def user_details(
    request: Request,
    user_id: UUID,
    service: UserService = Injected(UserService),
):
    # res2: AsyncTaskiqTask = await add_task_math2.kiq(
    #     x=5,
    #     y=5,
    # )
    # print(res2.task_id)
    #
    # res3: AsyncTaskiqTask = await post_processing_user.kiq(
    #     user_id=5
    # )
    # print(res3.task_id)
    res = await service.get_user(user_id)
    return success_response(res, request)

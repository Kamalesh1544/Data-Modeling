from uuid import UUID

from fastapi import APIRouter
from fastapi_injector import Injected

from src.app.db.models.user.user_model import UserModel
from src.app.routers.auth.services.user_services import UserService
from src.app.utils.response_helper import success_response
from src.app.utils.swagger_helper import generate_swagger_responses


router = APIRouter(tags=["User"])


@router.get(
    "/v1/user/{user_id}",
    responses=generate_swagger_responses(UserModel),
    summary="Get user details",
    description="Get user details by user id",
    openapi_extra={},
)
async def user_details(
    user_id: UUID, service: UserService = Injected(UserService)
):
    res = await service.get_user(user_id)
    return success_response(res)

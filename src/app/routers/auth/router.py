from fastapi import APIRouter
from fastapi_injector import Injected

from src.app.db.models.user.user_model import UserModel
from src.app.routers.auth.services.user_services import UserService
from src.app.utils.schemas.user_schemas import UserSchema

router = APIRouter(
    prefix="/user",
    tags=['User']
)


@router.get("/{user_id}", response_model=UserSchema)
async def me(user_id: int, service: UserService = Injected(UserService)):
    res = await service.get_user(user_id)
    return res

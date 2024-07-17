from uuid import UUID
from injector import inject, singleton

from src.app.db.models.user.user_model import UserModel
from src.app.routers.auth.repositories.user_repository import UserRepository
from src.app.utils.schemas.user_schemas import UserSchema


@singleton
class UserService:
    @inject
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    async def get_user(self, user_id:UUID)->UserModel :
        """
        Get user by id
        Args:
            user_id: user id

        Returns:
            UserModel: user model instance
        """
        print(f"----------------------------->{self._user_repo}")
        model = await self._user_repo.get_user(user_id)
        print(f"----------------------------->{model}")
        return model

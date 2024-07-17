from injector import inject, singleton

from src.app.db.models.user.user_model import UserModel
from src.app.routers.auth.repositories.user_repository import UserRepository
from src.app.utils.schemas.user_schemas import UserSchema


@singleton
class UserService:
    @inject
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    async def get_user(self, user_id: int) -> UserSchema:
        """
        Get user by id
        Args:
            user_id: user id

        Returns:
            UserModel: user model instance
        """

        # model = await self._user_repo.get_user(user_id)
        data = {
            "name": "hello",
            "role": "admin",
            "company": 1,
            "uuid": "hello",
            "user_id": "hello",
            "email": "hello",
            "email_verified": True,
            "firebase": {},
            "uid": "hello",
            "created_at": "2021-09-01T00:00:00"
        }
        return UserSchema(**data)

from uuid import UUID

from fastapi.exceptions import HTTPException
from injector import singleton

from src.app.core.exceptions.resources_exceptions import ResourceNotFoundError
from src.app.db.models.user.user_model import UserTable, UserModel


@singleton
class UserRepository:
    async def get_user(self, user_id: UUID) -> UserModel:
        """
        Get user by id
        Args:
            user_id: user id

        Returns:
            UserModel: user model instance

        Raises:
            HTTPException: if user not found
        """
        # No need to check if user is None, it will raise DoesNotExist exception
        model = UserTable.get(user_id=user_id)

        return await UserModel.from_queryset_single(model)

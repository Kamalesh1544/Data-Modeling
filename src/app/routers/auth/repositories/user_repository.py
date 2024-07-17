from injector import inject, singleton
from fastapi.exceptions import HTTPException

from src.app.db.models.user.user_model import UserTable, UserModel


@singleton
class UserRepository:
    async def get_user(self, user_id: int) -> UserModel:
        """
        Get user by id
        Args:
            user_id: user id

        Returns:
            UserModel: user model instance

        Raises:
            HTTPException: if user not found
        """

        model = UserTable.get_or_none(id=user_id)
        if not model:
            raise HTTPException(status_code=404, detail="User not found")

        return await UserModel.from_tortoise_orm(model)

from uuid import UUID
from injector import inject, singleton
from fastapi.exceptions import HTTPException

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

        print(f"----------------------------->{UserTable}")
        model =  UserTable.get(user_id=user_id)
        print(f"----------------------------->{model}")
        if not model:
            raise HTTPException(status_code=404, detail="User not found")

        return await UserModel.from_tortoise_orm(model)

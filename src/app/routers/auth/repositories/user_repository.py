from uuid import UUID

from injector import singleton

from src.app.db.models.user.user_model import UserModel, UserTable


@singleton
class UserRepository:
    """
    Repository class for user-related database operations.

    This class provides methods to interact with the user data
    stored in the database.
    """

    async def get_user(self, user_id: UUID) -> UserModel:
        """
        Retrieves a user by their unique identifier (UUID).

        Args:
            user_id (UUID): The unique identifier of the user.

        Returns:
            UserModel: An instance of the UserModel containing the user data.

        Raises:
            DoesNotExist: If the user is not found.
        """
        model = await UserTable.get(user_id=user_id)
        # Convert the retrieved database model into a UserModel instance.
        return await UserModel.from_queryset_single(model)

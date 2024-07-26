from uuid import UUID

from src.app.routers.auth.repositories.abstract_user_repo import (
    UserRepoAbstract,
)
from src.app.routers.auth.schemas.user_schemas import UserSchema


class FakeUserRepo(UserRepoAbstract):
    async def get_user(self, user_id: UUID) -> UserSchema:
        return UserSchema(
            user_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
            fullname="testuser",
            phone="1234567890",
            token="",
            type=0,
            email="testuser@example.com",
        )

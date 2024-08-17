from fastapi import Request
from strawberry.fastapi import BaseContext

from src.app.utils.schemas.user_schemas import AuthUserSchema


class CustomContext(BaseContext):
    def __init__(self, request: Request, user: AuthUserSchema):
        super().__init__()
        self.request = request
        self.user = user

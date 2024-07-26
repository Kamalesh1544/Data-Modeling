from uuid import UUID

from pydantic import BaseModel


class UserSchema(BaseModel):
    user_id: UUID
    email: str
    fullname: str
    phone: str
    token: str
    type: int

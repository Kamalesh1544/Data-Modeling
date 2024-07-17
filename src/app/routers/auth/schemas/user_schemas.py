from pydantic import BaseModel


class UserResponse(BaseModel):
    name: str
    role: str
    company: int
    uuid: str
    user_id: str
    email: str
    email_verified: bool
    firebase: dict
    uid: str
    created_at: str
    updated_at: str
    deleted_at: str
    id: int

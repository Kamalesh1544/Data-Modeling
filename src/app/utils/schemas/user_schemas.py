from pydantic import BaseModel


class UserSchema(BaseModel):
    name: str
    role: str
    company: int
    uuid: str
    user_id: str
    email: str
    email_verified: bool
    firebase: dict
    uid: str

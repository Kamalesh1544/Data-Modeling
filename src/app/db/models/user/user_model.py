from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

from src.app.db.models.inheritance_model import TimestampMixin
from src.app.db.models.user.user_constants import UserTypesConst


class UserTable(TimestampMixin, models.Model):
    user_id = fields.UUIDField(pk=True, generated=False)
    email = fields.CharField(index=True, unique=True, null=False, max_length=255)
    fullname = fields.CharField(max_length=1000, default="")
    phone = fields.CharField(max_length=100, default="")
    token = fields.CharField(max_length=1000, default="", index=True)
    type = fields.IntField(max_length=1000, default=UserTypesConst.USER)

    def __str__(self):
        return self.fullname

    class Meta:
        table = "t_user"
        # unique_together=(("field_a", "field_b"), )

    class PydanticMeta:
        exclude = ["created_at", "updated_at", "status"]


UserModel = pydantic_model_creator(UserTable, name="User")

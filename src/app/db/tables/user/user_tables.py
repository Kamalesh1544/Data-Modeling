from tortoise import fields, models

from src.app.db.tables.inheritance_table import TimestampMixin
from src.app.db.tables.user.user_constants import UserTypesConst


class UserTable(TimestampMixin, models.Model):
    user_id = fields.UUIDField(primary_key=True, generated=False)
    email = fields.CharField(
        db_index=True, unique=True, null=False, max_length=255
    )
    fullname = fields.CharField(max_length=1000, default="")
    phone = fields.CharField(max_length=100, default="")
    token = fields.CharField(max_length=1000, default="", db_index=True)
    type = fields.IntField(max_length=1000, default=UserTypesConst.USER)

    def __str__(self):
        return self.fullname

    class Meta:
        table = "t_user"
        # unique_together=(("field_a", "field_b"), )

    class PydanticMeta:
        exclude = ["created_at", "status"]

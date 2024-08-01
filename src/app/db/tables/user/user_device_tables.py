from tortoise import fields, models

from src.app.db.tables.inheritance_table import TimestampMixin
from src.app.db.tables.user.user_constants import UserTableConst


class UserDeviceTable(TimestampMixin, models.Model):
    id = fields.IntField(pk=True)
    device_name = fields.CharField(max_length=100, default="")
    device_id = fields.CharField(max_length=100, default="")
    location = fields.CharField(max_length=100, default="")

    user = fields.ForeignKeyField(UserTableConst.USER_TABLE, related_name="device_user")

    def __str__(self):
        return self.device_name

    class Meta:
        table = "t_user_devices"

    class PydanticMeta:
        exclude = ["created_at", "updated_at", "status"]

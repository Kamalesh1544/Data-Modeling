from tortoise import fields


class TimestampMixin:
    # dates
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    modified_at = fields.DatetimeField(null=True, auto_now=True)
    # row status
    status = fields.BooleanField(default=True)

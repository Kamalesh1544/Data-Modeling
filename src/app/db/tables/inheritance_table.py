from tortoise import fields, models


class TimestampMixin(models.Model):
    # dates
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    modified_at = fields.DatetimeField(null=True, auto_now=True)
    # row status
    status = fields.BooleanField(default=True)

    class Meta:
        abstract = True

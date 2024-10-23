from tortoise import fields, models


class TimestampMixin(models.Model):
    """
    A mixin class that adds timestamp fields and a status field to a model.

    Attributes:
        created_at (DatetimeField): The date and time when the record was created.
            Automatically set to the current date and time when the record is first created.
        modified_at (DatetimeField): The date and time when the record was last modified.
            Automatically updated to the current date and time whenever the record is saved.
        status (BooleanField): A boolean field indicating the status of the record.
            Defaults to True.

    Meta:
        abstract (bool): Indicates that this is an abstract base class.
    """

    # dates
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    modified_at = fields.DatetimeField(null=True, auto_now=True)
    # row status
    status = fields.BooleanField(default=True)

    class Meta:
        abstract = True

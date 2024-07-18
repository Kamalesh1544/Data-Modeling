class UserTypesConst:
    ADMIN = 0
    USER = 1


# All the tables inside this module
# To create relation with other module
class UserTableConst:
    USER_TABLE = "models.UserTable"
    DEVICE_TABLE = "models.UserDeviceTable"


# All the tables inside this module will be registered
USER_TABLES = [
    "src.app.db.models.user.user_model",
    "src.app.db.models.user.user_device_model",
]

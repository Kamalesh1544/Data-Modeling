from src.app.core.exceptions.general_eception import GeneralException


class UserAccountError(GeneralException):

    def __init__(self, message="User account is disabled, please contact support"):
        self.message = message
        self.status_code = 403
        self.error_code = "USER_ACCOUNT_DISABLE"
        super().__init__(
            message=self.message,
            status_code=self.status_code,
            error_code=self.error_code
        )


class UserPermissionError(GeneralException):

    def __init__(self, message="user don't have sufficient permission"):
        self.message = message
        self.status_code = 403
        self.error_code = "PERMISSION_ERROR"
        super().__init__(
            message=self.message,
            status_code=self.status_code,
            error_code=self.error_code
        )

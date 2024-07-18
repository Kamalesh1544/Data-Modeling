from src.app.core.exceptions.general_exception import GeneralException


class ResourceNotFoundError(GeneralException):
    def __init__(self, message="Resources not found"):
        self.message = message
        self.status_code = 404
        self.error_code = "RESOURCE_NOT_FOUND"
        super().__init__(
            message=self.message,
            status_code=self.status_code,
            error_code=self.error_code,
        )

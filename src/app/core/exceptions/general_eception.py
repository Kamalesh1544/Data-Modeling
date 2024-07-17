from src.app.utils.schemas.output_schemas import ErrorSchemas


class GeneralException(Exception):
    """
    Base class for other exceptions
    """

    def __init__(self, message="An error occurred", status_code=400, error_code="APP_ERROR",
                 details: list[ErrorSchemas] = None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details
        super().__init__(self.message)

    def __str__(self):
        return "message: " + self.message + " status_code: " + str(self.status_code) + " error_code: " + self.error_code

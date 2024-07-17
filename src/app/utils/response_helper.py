from typing import TypeVar

from pydantic import BaseModel

from src.app.utils.schemas.output_schemas import ErrorResponse, SuccessResponse, ErrorOutputSchema, ErrorSchemas

T = TypeVar('T', bound=BaseModel)


def success_response(res: T):
    return SuccessResponse(data=res)


def error_response(error_code: str, message: str = "", details: list[ErrorSchemas] = None):
    return ErrorResponse(
        error=ErrorOutputSchema(
            code=error_code,
            message=message,
            details=details if details else []
        )
    )

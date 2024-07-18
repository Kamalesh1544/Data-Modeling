from typing import TypeVar

from pydantic import BaseModel
from starlette.responses import JSONResponse

from src.app.utils.schemas.output_schemas import ErrorResponse, SuccessResponse, ErrorOutputSchema, ErrorSchemas

T = TypeVar('T', bound=BaseModel)


def success_response(res: T, message: str = "", status_code: int = 200):
    response = SuccessResponse(data=res)
    if message:
        SuccessResponse(data=res, metadata={"message": message}).model_dump()

    return JSONResponse(response.model_dump(), status_code=status_code)


def error_response(error_code: str, message: str = "", details: list[ErrorSchemas] = None, status_code: int = 400):
    error = ErrorResponse(
        error=ErrorOutputSchema(
            code=error_code,
            message=message,
            details=details if details else []
        )
    )
    return JSONResponse(error.model_dump(), status_code=status_code)

from typing import TypeVar

from fastapi import Request
from pydantic import BaseModel
from starlette.responses import JSONResponse

from src.app.utils.schemas.output_schemas import (
    ErrorOutputSchema,
    ErrorResponse,
    ErrorSchemas,
    SuccessResponse,
)


T = TypeVar("T", bound=BaseModel)


def success_response(
    res: T, request: Request, message: str = "OK", status_code: int = 200
):
    metadata = {
        "request_id": request.state.request_id,
        "timestamp": request.state.timestamp,
        "message": message,
    }
    response: SuccessResponse = SuccessResponse(data=res, metadata=metadata)
    return JSONResponse(response.model_dump(), status_code=status_code)


def error_response(
    request: Request,
    error_code: str,
    message: str = "",
    details: list[ErrorSchemas] | None = None,
    status_code: int = 400,
):
    metadata = {
        "request_id": request.state.request_id,
        "timestamp": request.state.timestamp,
        "message": "Failed",
    }
    error = ErrorResponse(
        error=ErrorOutputSchema(
            code=error_code, message=message, details=details if details else []
        ),
        metadata=metadata,
    )
    return JSONResponse(error.model_dump(), status_code=status_code)

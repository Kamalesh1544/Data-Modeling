from typing import Any, TypeVar

from fastapi import Request
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel

from src.app.utils.schemas.output_schemas import (
    ErrorOutputSchema,
    ErrorResponse,
    ErrorSchemas,
    SuccessResponse,
)


T = TypeVar("T", bound=BaseModel)


def merge_metadata(
    metadata: dict[Any, Any] | None, request: Request, message: str = ""
) -> dict[Any, Any]:
    if metadata:
        metadata.update(
            {
                "request_id": request.state.request_id,
                "timestamp": request.state.timestamp,
                "message": message,
            }
        )
        return metadata

    return {
        "request_id": request.state.request_id,
        "timestamp": request.state.timestamp,
        "message": message,
    }


def success_response(
    res: T | None,
    request: Request,
    message: str = "OK",
    status_code: int = 200,
    metadata: dict | None = None,
):
    """
    Creates a success response with the provided data, message,
    status code, and metadata.

    Parameters:
    - res (T | None): The data to be included in the response.
    - request (Request): The FastAPI request object.
    - message (str): The message associated with the response (default is "OK").
    - status_code (int): The HTTP status code of the response (default is 200).
    - metadata (dict): Additional metadata to be merged with the response.

    Returns:
    - ORJSONResponse: The JSON response containing the data, message,
            and metadata.
    """
    response: SuccessResponse = SuccessResponse(
        data=res, metadata=merge_metadata(metadata, request, message)
    )
    return ORJSONResponse(response.model_dump(), status_code=status_code)


# ruff: noqa: PLR0913
def error_response(
    request: Request,
    error_code: str,
    message: str = "",
    details: list[ErrorSchemas] | None = None,
    status_code: int = 400,
    metadata: dict | None = None,
):
    """
    Creates an error response with the provided error code, message,
    details, status code, and metadata.

    Parameters:
    - request (Request): The FastAPI request object.
    - error_code (str): The code associated with the error.
    - message (str): The message describing the error
        (default is an empty string).
    - details (list[ErrorSchemas] | None): Additional details about the error
            (default is None).
    - status_code (int): The HTTP status code of the response (default is 400).
    - metadata (dict): Additional metadata to be merged with the response.

    Returns:
    - ORJSONResponse: The JSON response containing the error details, message,
            and metadata.
    """
    error = ErrorResponse(
        error=ErrorOutputSchema(
            code=error_code, message=message, details=details if details else []
        ),
        metadata=merge_metadata(metadata, request, message),
    )
    return ORJSONResponse(error.model_dump(), status_code=status_code)

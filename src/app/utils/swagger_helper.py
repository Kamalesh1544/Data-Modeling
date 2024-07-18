from typing import TypeVar, Dict, Any, Generic
from datetime import datetime
from pydantic import BaseModel
import uuid

from src.app.utils.schemas.output_schemas import ErrorResponse, ErrorSchemas, ErrorOutputSchema

T = TypeVar('T')


class _SwaggerSuccessSchemas(BaseModel, Generic[T]):
    data: T
    metadata: dict = {
        "message": "Success",
        "request_id": uuid.uuid4().hex,
        "timestamp": datetime.now().isoformat()
    }


class _SwaggerError400Schemas(BaseModel):
    metadata: dict = {
        "message": "Failed",
        "request_id": uuid.uuid4().hex,
        "timestamp": datetime.now().isoformat()
    }
    error: ErrorOutputSchema = ErrorOutputSchema(
        code="RESOURCE_NOT_FOUND",
        message="Resource not found",
        details=[]
    )


class _SwaggerError401Schemas(BaseModel):
    metadata: dict = {
        "message": "Failed",
        "request_id": uuid.uuid4().hex,
        "timestamp": datetime.now().isoformat()
    }
    error: ErrorOutputSchema = ErrorOutputSchema(
        code="AUTHENTICATION_FAILED",
        message="Please provide valid credentials",
        details=[]
    )


class _SwaggerError403Schemas(BaseModel):
    metadata: dict = {
        "message": "Failed",
        "request_id": uuid.uuid4().hex,
        "timestamp": datetime.now().isoformat()
    }
    error: ErrorOutputSchema = ErrorOutputSchema(
        code="PERMISSION_ERROR",
        message="You don't have permission to access this resource",
        details=[]
    )


class _SwaggerError426Schemas(BaseModel):
    metadata: dict = {
        "message": "Failed",
        "request_id": uuid.uuid4().hex,
        "timestamp": datetime.now().isoformat()
    }
    error: ErrorOutputSchema = ErrorOutputSchema(
        code="VALIDATION_ERROR",
        message="Invalid input",
        details=[
            ErrorSchemas(
                loc=["body", "name"],
                msg="field required",
                type="value_error.missing"
            )
        ]
    )


def generate_swagger_responses(model: T) -> Dict[int, Dict[str, Any]]:
    return {
        400: {"model": _SwaggerError400Schemas, "description": "Invalid input"},
        404: {"model": _SwaggerError400Schemas, "description": "Resource not found"},
        401: {"model": _SwaggerError401Schemas, "description": "Authentication failed"},
        403: {"model": _SwaggerError403Schemas, "description": "Forbidden"},
        422: {"model": _SwaggerError426Schemas, "description": "Validation error"},
        200: {
            "model": _SwaggerSuccessSchemas[model],
        }
    }


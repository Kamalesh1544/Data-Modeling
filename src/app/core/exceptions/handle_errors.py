import logging
from enum import Enum
from typing import Any, Generic, TypeVar
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from tortoise.exceptions import DoesNotExist, IntegrityError
from pydantic import BaseModel

from src.app.core.exceptions.rbac.user_exception import UserAccountDisableError, UserWritePermissionError
from src.app.utils.response_helper import error_response
from src.app.utils.schemas.output_schemas import ErrorSchemas

logger = logging.getLogger("exception")


def init_errors_handler(app: FastAPI):
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        logger.error("HTTP exception" + str(request.base_url), exc_info=exc)
        error = error_response(
            error_code="HTTPException",
            message=str(exc.detail)
        )
        return JSONResponse(
            error.dict(),
            status_code=exc.status_code
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.error("Value error exception" + str(request.base_url), exc_info=exc)
        details = [ErrorSchemas(**error) for error in exc.errors()]
        error = error_response(
            error_code="VALIDATION_ERROR",
            message=str(exc.body),
            details=details
        )
        return JSONResponse(error.dict(), status_code=422)

    @app.exception_handler(DoesNotExist)
    async def not_found_exception_handler(request: Request, exc: DoesNotExist):
        logger.error("Not found exception" + str(request.base_url), exc_info=exc)
        error = error_response(
            error_code="RESOURCE_NOT_FOUND",
            message=exc.TEMPLATE,
        )
        return JSONResponse(error.dict(), status_code=404)

    @app.exception_handler(IntegrityError)
    async def not_found_exception_handler(request: Request, exc: IntegrityError):
        logger.error("Integrity exception" + str(request.base_url), exc_info=exc)
        error = error_response(
            error_code="INTEGRITY_ERROR",
            message=str(exc),
        )
        return JSONResponse(error.dict(), status_code=400)

    ########################################
    ##### Custom exception handler here ####
    ########################################
    @app.exception_handler(UserAccountDisableError)
    async def user_account_exception_handler(request: Request, exc: Exception):
        logger.error("Value error exception" + str(request.base_url), exc_info=exc)
        return JSONResponse(error_response(str(exc)).dict(), status_code=403)

    @app.exception_handler(UserWritePermissionError)
    async def user_write_exception_handler(request: Request, exc: Exception):
        logger.error("Value error exception" + str(request.base_url), exc_info=exc)
        return JSONResponse(error_response(str(exc)).dict(), status_code=403)



# value error
#  RessourcesNotFoundError

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

logger = logging.getLogger("exception")

class ResponseType(str, Enum):
    failed = "FAILED"
    successful = "OK"


T = TypeVar('T')

class OutputResponse(BaseModel, Generic[T]):
    data: T = None
    message: str = ""
    response: ResponseType = ResponseType.successful


def error_response(message: str):
    return OutputResponse(
        message=message,
        response=ResponseType.failed
    )



def init_errors_handler(app: FastAPI):
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: Exception):
        logger.error("HTTP exception" + str(request.base_url), exc_info=exc)
        return JSONResponse(error_response(str(exc)).dict(), status_code=401)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: Exception):
        logger.error("Value error exception" + str(request.base_url), exc_info=exc)
        return JSONResponse(error_response(str(exc)).dict(), status_code=422)

    @app.exception_handler(DoesNotExist)
    async def not_found_exception_handler(request: Request, exc: Exception):
        logger.error("Not found exception" + str(request.base_url), exc_info=exc)
        return JSONResponse(error_response(str(exc)).dict(), status_code=404)

    @app.exception_handler(IntegrityError)
    async def not_found_exception_handler(request: Request, exc: Exception):
        logger.error("Integrity exception" + str(request.base_url), exc_info=exc)
        return JSONResponse(error_response(str(exc)).dict(), status_code=404)

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

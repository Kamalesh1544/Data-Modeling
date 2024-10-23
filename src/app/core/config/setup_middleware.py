import uuid
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from src.app.core import get_settings


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Generate request ID and timestamp
        request_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()

        # Add request ID and timestamp to request headers
        request.state.request_id = request_id
        request.state.timestamp = timestamp

        # Proceed with the request
        response = await call_next(request)

        # Add request ID and timestamp to response headers for logging
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Timestamp"] = timestamp

        return response


def setup_middleware(app: FastAPI):
    """
    Set up middleware for the FastAPI application.

    Args:
        app (FastAPI): The FastAPI application instance.

    Middleware:
        - CORS: Configured based on settings.ORIGINS.
        - TrustedHost: Configured with allowed hosts from settings.ALLOWED_HOST.
        - GZip: Applied with a minimum size of 1000 bytes.
    """
    settings = get_settings()
    # init cors
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ORIGINS.split(","),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOST.split(","))

    app.add_middleware(RequestIDMiddleware)

    app.add_middleware(GZipMiddleware, minimum_size=1000)

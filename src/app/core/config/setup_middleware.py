from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.cors import CORSMiddleware

from src.app.core.config.settings import get_settings


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

    app.add_middleware(
        TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOST.split(",")
    )

    app.add_middleware(GZipMiddleware, minimum_size=1000)

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from src.app.core.config.settings import get_settings


def setup_middleware(app: FastAPI):
    settings = get_settings()
    # init cors
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ORIGINS.split(","),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # app.add_middleware(
    #     TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS.split(",")
    # )

    app.add_middleware(GZipMiddleware, minimum_size=1000)

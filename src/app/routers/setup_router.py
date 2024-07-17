from fastapi import FastAPI

from .auth import router as auth_router


def init_routes(app: FastAPI):
    app.include_router(auth_router.router)
    # crud router

from fastapi import FastAPI

from .auth import router as auth_router
from .graphql.router import graphql_app


def init_routes(app: FastAPI):
    app.include_router(auth_router.router)
    # crud router
    app.include_router(graphql_app, prefix="/gql")

from fastapi import FastAPI

from src.app.routers.auth import get_router as get_auth_router
from src.app.routers.document import get_router as get_document_router
from src.app.routers.graph import get_router as get_graph_router
from src.app.routers.relational import get_router as get_relational_router


def init_routes(app: FastAPI):
    app.include_router(get_auth_router())
    app.include_router(get_relational_router())
    app.include_router(get_document_router())
    app.include_router(get_graph_router())


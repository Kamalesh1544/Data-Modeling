from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from injectq.integrations.fastapi import InjectFastAPI

from src.app.core.auth import get_current_user
from src.app.routers.graph.init_db.services.init_db_service import (
    InitDBService,
)
from src.app.utils.schemas import AuthUserSchema


router = APIRouter(tags=["Neo4j — Initialization"])


@router.post("/init")
async def init_graph(
    user: AuthUserSchema = Depends(get_current_user),
    service: Annotated[InitDBService, InjectFastAPI(InitDBService)] = None,  # type: ignore[assignment]
) -> dict[str, str]:
    return await service.init_database()


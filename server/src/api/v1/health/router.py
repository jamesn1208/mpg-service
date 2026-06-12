from fastapi import APIRouter

from api.core.deps.database import DB_SESSION
from . import schemas, service

router = APIRouter(prefix='/health',
                   tags=['Health'])


@router.get('/database', status_code=200)
async def is_the_database_healthy(session: DB_SESSION) -> schemas.HealthReport:
    return await service.get_database_health(session)


@router.get('/liveness', status_code=200)
async def is_the_api_alive() -> schemas.HealthReport:
    return schemas.HealthReport(status="ok",
                                message="API is alive.")

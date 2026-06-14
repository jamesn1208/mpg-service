from fastapi import APIRouter

from api.core.deps.database import DB_SESSION
from api.core.deps.auth import USER_ID
from . import schemas, service

router = APIRouter(prefix='/metrics',
                   tags=['Metrics'])


@router.get('', status_code=200)
async def get_metrics(session: DB_SESSION,
                      user_id: USER_ID) -> list[schemas.Metric]:
    return await service.get_metrics(session=session,
                                     user_id=user_id)

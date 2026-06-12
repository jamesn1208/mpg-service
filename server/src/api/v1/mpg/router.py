from fastapi import APIRouter

from api.core.deps.database import DB_SESSION
from api.core.deps.auth import USER_ID
from api.core.schemas import ActionResponse, LIMIT, OFFSET
from . import schemas, service

router = APIRouter(prefix='/mpg',
                   tags=['MPG'])


@router.get('')
async def get_all_mpg_history(session: DB_SESSION,
                              user_id: USER_ID,
                              limit: LIMIT = 10,
                              offset: OFFSET = 0) -> list[schemas.MPGLog]:

    return await service.get_all_mpg_history(limit=limit,
                                             offset=offset,
                                             session=session,
                                             user_id=user_id)


@router.get('/{registration}')
async def get_mpg_history_by_registration(session: DB_SESSION,
                                           user_id: USER_ID,
                                           registration: str,
                                           limit: LIMIT = 10,
                                           offset: OFFSET = 0) -> list[schemas.MPGLog]:
    return await service.get_mpg_history_by_registration(limit=limit,
                                                         offset=offset,
                                                         session=session,
                                                         user_id=user_id,
                                                         registration=registration)


@router.post('', status_code=201)
async def log_mpg(log: schemas.MPGLog,
                  session: DB_SESSION,
                  user_id: USER_ID) -> ActionResponse:
    return await service.log_mpg(log=log,
                                 session=session,
                                 user_id=user_id)

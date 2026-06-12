from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
import logging

from api.core.schemas import ActionResponse
from api.core.exceptions import ActionError
from . import schemas, models


async def log_mpg(log: schemas.MPGLog,
                  session: AsyncSession,
                  user_id: int) -> ActionResponse:
    if not await models.is_vehicle_registered_to_user(registration=log.registration,
                                                      session=session,
                                                      user_id=user_id):
        raise ActionError(status_code=400,
                          message="The provided vehicle registration is not registered to you.")

    try:
        await models.insert_mpg_log(log=log,
                                    session=session,
                                    user_id=user_id)
    except IntegrityError:
        logging.exception("Got IntegrityError whilst inserting log data into database.")
        raise ActionError(status_code=500,
                          message="Failed to insert MPG log data.")

    return ActionResponse(success=True,
                          message="Successfully inserted MPG log data.")


async def get_all_mpg_history(limit: int,
                              offset: int,
                              session: AsyncSession,
                              user_id: int) -> list[schemas.MPGLog]:
    data = await models.get_all_mpg_history(limit=limit,
                                            offset=offset,
                                            session=session,
                                            user_id=user_id)

    return [
        schemas.MPGLog(registration=l.registration,
                       date=l.date.strftime("%Y-%m-%d"),
                       litres=l.litres,
                       mpg=l.mpg,
                       miles=l.miles,
                       total_cost=l.total_cost)
        for l in data
    ]


async def get_mpg_history_by_registration(limit: int,
                                          offset: int,
                                          session: AsyncSession,
                                          user_id: int,
                                          registration: str) -> list[schemas.MPGLog]:
    data = await models.get_mpg_history_by_registration(limit=limit,
                                                        offset=offset,
                                                        session=session,
                                                        user_id=user_id,
                                                        registration=registration)

    return [
        schemas.MPGLog(registration=l.registration,
                       date=l.date.strftime("%Y-%m-%d"),
                       litres=l.litres,
                       mpg=l.mpg,
                       miles=l.miles,
                       total_cost=l.total_cost)
        for l in data
    ]

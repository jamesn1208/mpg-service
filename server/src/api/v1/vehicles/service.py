from sqlalchemy.ext.asyncio import AsyncSession

from . import schemas, models
from api.core.exceptions import MissingData
from api.core.schemas import ActionResponse


async def get_vehicles(session: AsyncSession,
                       user_id: int,
                       limit: int,
                       offset: int) -> list[schemas.Vehicle]:

    data = await models.get_vehicles_by_user_id(user_id=user_id,
                                                limit=limit,
                                                offset=offset,
                                                session=session)

    return [schemas.Vehicle(registration=vehicle.registration,
                            make=vehicle.make,
                            emissions=vehicle.emissions,
                            year=vehicle.year,
                            colour=vehicle.colour) for vehicle in data]


async def get_vehicle(session: AsyncSession,
                      user_id: int,
                      registration: str) -> schemas.Vehicle:

    vehicle = await models.get_vehicle_by_user_id_and_registration(user_id=user_id,
                                                                   registration=registration,
                                                                   session=session)

    if vehicle is None:
        raise MissingData(message=f"Could not locate any vehicle with registration '{registration}'.")

    return schemas.Vehicle(registration=vehicle.registration,
                           make=vehicle.make,
                           emissions=vehicle.emissions,
                           year=vehicle.year,
                           colour=vehicle.colour)


async def add_vehicle(session: AsyncSession,
                      vehicle: schemas.Vehicle,
                      user_id: int) -> ActionResponse:

    await models.add_vehicle(session=session,
                             vehicle=vehicle,
                             user_id=user_id)

    return ActionResponse(success=True,
                          message=f"Vehicle added successfully.")

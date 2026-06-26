import logging
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from . import schemas, models
from api.core import config
from api.core.exceptions import MissingData, ActionError
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


async def lookup_vehicle(registration: str, client: AsyncClient) -> schemas.Vehicle:
    payload = {
        "registrationNumber": registration
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": config.VES_API_KEY
    }

    try:
        response = await client.post(url="https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles",
                                     headers=headers,
                                     json=payload,
                                     timeout=15)

        if response.status_code == 404:
            raise ActionError(message="Vehicle not found.",
                              status_code=404)
        elif 200 > response.status_code >= 300:
            raise RuntimeError("Unable to get vehicle data from VES DVLA API.")
    except Exception as ex:
        raise ActionError(message="Unable to get vehicle information from the DVLA.",
                          status_code=500) from ex

    data = response.json()

    try:
        vehicle = schemas.Vehicle(registration=registration,
                                  make=data.get('make', ''),
                                  colour=str(data.get('colour', '')).capitalize(),
                                  year=data.get('yearOfManufacture', 0),
                                  emissions=data.get('co2Emissions', 0))
    except KeyError as e:
        logging.exception("Failed to create Vehicle object.")
        raise ActionError(status_code=500,
                          message="DVLA data is partially missing.") from e

    return vehicle


async def update_vehicle(session: AsyncSession,
                         new_data: schemas.VehicleUpdate,
                         registration: str) -> ActionResponse:

    if new_data.emissions is None and new_data.make is None and new_data.year is None and new_data.colour is None:
        raise MissingData(message="Nothing to update.")

    vehicle = await models.get_vehicle_by_registration(registration=registration,
                                                       session=session)

    if vehicle is None:
        raise MissingData(message=f"Could not locate any vehicle with registration '{registration}'.")

    if (vehicle.make == new_data.make
        and vehicle.year == new_data.year
        and vehicle.colour == new_data.colour
        and vehicle.emissions == new_data.emissions):
        raise MissingData(message="Nothing to update.")

    if new_data.emissions is not None:
        vehicle.emissions = new_data.emissions
    if new_data.year is not None:
        vehicle.year = new_data.year
    if new_data.colour is not None:
        vehicle.colour = new_data.colour
    if new_data.make is not None:
        vehicle.make = new_data.make

    await session.flush()

    return ActionResponse(message='Successfully updated vehicle information.',
                          success=True)


async def unlink_vehicle(session: AsyncSession,
                         user_id: int,
                         registration: str) -> ActionResponse:

    vehicle = await models.get_vehicle_by_user_id_and_registration(registration=registration,
                                                                   user_id=user_id,
                                                                   session=session)

    if vehicle is None:
        raise MissingData(message=f"Could not locate any vehicle with registration '{registration}' linked to your account.")

    await models.unlink_vehicle(registration=registration,
                                user_id=user_id,
                                session=session)

    return ActionResponse(message='Successfully unlinked vehicle.',
                          success=True)

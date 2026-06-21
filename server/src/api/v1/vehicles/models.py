from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy import select

from api.core.models import Vehicles, VehicleOwnership
from . import schemas


async def get_vehicles_by_user_id(user_id: int, limit: int, offset: int, session: AsyncSession) -> list[Vehicles]:
    """
    Get a list of vehicles owned by a given user with pagination.

    :param user_id: The user_id of the vehicle owner.
    :param limit: The amount of vehicles to return.
    :param offset: The current page number (0 indexed).
    :param session: The database session.
    :return: List of Vehicles instances.
    """
    try:
        return (await session.execute(  # type: ignore
            select(Vehicles).
            join(VehicleOwnership)
            .where(VehicleOwnership.user_id == user_id)
            .limit(limit)
            .offset(offset * limit))).scalars()
    except NoResultFound:
        return []


async def get_vehicle_by_user_id_and_registration(user_id: int, registration: str, session: AsyncSession) -> Vehicles | None:
    """
    Get a vehicle by its registration number & user_id.

    :param user_id: The user_id of the vehicle owner.
    :param registration: The registration number of the vehicle.
    :param session: The database session.
    :return: Instance of Vehicles or None.
    """
    try:
        return (await session.execute(
            select(Vehicles).
            join(VehicleOwnership)
            .where(VehicleOwnership.user_id == user_id)
            .where(Vehicles.registration == registration))).scalar_one()
    except NoResultFound:
        return None


async def add_vehicle(vehicle: schemas.Vehicle, user_id: int, session: AsyncSession) -> None:
    """
    Maps an existing vehicle to another user, or creates a new one, then maps it to the user.

    :param vehicle: The vehicle to add.
    :param user_id: The user_id of the vehicle owner.
    :param session: The database session.
    :return: Nothing.
    """
    ownership_data = VehicleOwnership(registration=vehicle.registration,
                                      user_id=user_id)

    try:
        # Attempt to add relationship to VehicleOwnership table
        session.add(ownership_data)
        await session.flush()
    except IntegrityError:
        # Rollback previous SQL (contains PrimaryKey violation)
        await session.rollback()

        # Add new vehicle to the Vehicles table
        vehicle_data = Vehicles(registration=str(vehicle.registration).upper(),
                                make=vehicle.make,
                                emissions=vehicle.emissions,
                                year=vehicle.year,
                                colour=vehicle.colour)

        session.add(vehicle_data)
        await session.flush()

        # Call self to add ownership data after vehicle is added to Vehicles table
        await add_vehicle(vehicle=vehicle,
                          user_id=user_id,
                          session=session)

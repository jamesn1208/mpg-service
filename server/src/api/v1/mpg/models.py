from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.exc import NoResultFound
from datetime import datetime

from api.core.models import MPGLog, VehicleOwnership
from . import schemas


async def is_vehicle_registered_to_user(registration: str,
                                        user_id: int,
                                        session: AsyncSession) -> bool:
    """
    Check if the vehicle provided is registered to the user.

    :param registration: The vehicle registration number to check.
    :param user_id: The user_id to check against.
    :param session: The database session to use.
    :return: True if the vehicle is registered to the user, False otherwise.
    """
    try:
        (await session.execute(
            select(VehicleOwnership)
            .where(
                VehicleOwnership.user_id == user_id,
                VehicleOwnership.registration == registration))
         ).one()
    except NoResultFound:
        return False
    return True


async def insert_mpg_log(log: schemas.MPGLog,
                         session: AsyncSession,
                         user_id: int) -> None:
    """
    Insert a new MPG log entry into the database.

    :param log: MPGLog schema containing new log data.
    :param session: The database session to use.
    :param user_id: The user_id to associate with the entry.
    :return: Nothing.
    """
    log_entry = MPGLog(user_id=user_id,
                       registration=log.registration,
                       mpg=log.mpg,
                       litres=log.litres,
                       miles=log.miles,
                       total_cost=log.total_cost,
                       price_per_litre=round((log.total_cost * 100) / log.litres, 1),
                       date=datetime.strptime(log.date, "%Y-%m-%d"))
    session.add(log_entry)
    await session.flush()


async def get_all_mpg_history(limit: int,
                              offset: int,
                              session: AsyncSession,
                              user_id: int) -> schemas.MPGLogWrapperInt:
    """
    Get all MPG history for a given user_id with pagination.

    :param limit: The amount of records to return.
    :param offset: The page number based on limit (0 indexed)
    :param session: The database session to use.
    :param user_id: The user_id to query against.
    :return: An instance of MPGLogWrapperInt.
    """
    vehicles = (await session.execute(
        select(VehicleOwnership.registration)
        .where(
            VehicleOwnership.user_id == user_id
        )
    )).scalars().all()
    query = (select(MPGLog)
    .where(
        MPGLog.user_id == user_id
    ).filter(
        MPGLog.registration.in_(vehicles)
    ))

    try:
        data = (await session.execute(
            query
            .limit(limit)
            .offset(offset * limit)
            .order_by(MPGLog.date.desc())
        )).scalars().all()
        count = (await session.execute(
            select(
                func.count()
            ).select_from(query.subquery())
        )).scalar()
        session.expunge_all()

        return schemas.MPGLogWrapperInt(total=int(count), data=list(data))
    except NoResultFound:
        return schemas.MPGLogWrapperInt(total=0, data=[])


async def get_mpg_history_by_registration(limit: int,
                                          offset: int,
                                          session: AsyncSession,
                                          user_id: int,
                                          registration: str) -> schemas.MPGLogWrapperInt:
    """
    Get all MPG history for a given user_id with pagination.

    :param limit: The amount of records to return.
    :param offset: The page number based on limit (0 indexed)
    :param session: The database session to use.
    :param user_id: The user_id to query against.
    :param registration: The registration number to query against.
    :return: An instance of MPGLogWrapperInt.
    """
    query = (select(MPGLog)
    .where(
        MPGLog.user_id == user_id,
        MPGLog.registration == registration
    ))
    try:
        data = (await session.execute(
            query
            .limit(limit)
            .offset(offset * limit)
            .order_by(MPGLog.date.desc())
        )).scalars().all()
        count = (await session.execute(
            select(func.count())
            .select_from(query.subquery())
        )).scalar()
        session.expunge_all()

        return schemas.MPGLogWrapperInt(total=int(count),
                                        data=list(data))
    except NoResultFound:
        return schemas.MPGLogWrapperInt(total=0, data=[])

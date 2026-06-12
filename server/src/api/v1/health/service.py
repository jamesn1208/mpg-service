from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import logging

from . import schemas


async def get_database_health(session: AsyncSession) -> schemas.HealthReport:
    """
    Runs various database checks on the AsyncSession to determine if the database connections are healthy.

    :param session: The session to check.
    :return: HealthReport object
    """
    status = "ok"
    message = "Database connection is healthy."

    if not session.is_active:
        status = "error"
        message = "Database connections are not active."

    try:
        data = (await session.execute(text("SELECT 1"))).one()
        assert data[0] == 1, "Unexpected result returned by database."

    except (SQLAlchemyError, AssertionError, IndexError):
        logging.exception("Failed to run health query against database.")
        status = "error"
        message = "Database connections are unable to query the database."

    return schemas.HealthReport(status=status,  # type: ignore
                                message=message)

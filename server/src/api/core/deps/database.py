import logging
from fastapi import Request, Depends
from typing import Annotated, Any, AsyncGenerator
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


async def get_session(request: Request) -> AsyncGenerator[Any, Any]:
    try:
        async with request.app.state.database() as session:
            yield session
            await session.commit()
    except SQLAlchemyError:
        logging.exception("Failed whilst interacting with database session.")
        raise


type DB_SESSION = Annotated[AsyncSession, Depends(get_session)]

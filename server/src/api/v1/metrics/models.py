from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select
from typing import Any


async def get_metric(session: AsyncSession, query: Select[Any], params: dict[Any, Any]) -> Any:
    data = (await session.execute(query, params)).scalar_one()
    session.expunge_all()
    return data

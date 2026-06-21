from httpx import AsyncClient
from typing import AsyncGenerator, Annotated
from fastapi import Depends
import logging


async def get_web_client() -> AsyncGenerator[AsyncClient, None]:
    try:
        async with AsyncClient() as client:
            yield client
    except Exception:
        logging.exception("Error getting an async web client.")


type WEB_CLIENT = Annotated[AsyncClient, Depends(get_web_client)]

from logging import INFO, DEBUG
from os import environ
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


ENVIRONMENT = environ.get("ENVIRONMENT", "DEV")

LOGGING_LEVEL = INFO if ENVIRONMENT == "PROD" else DEBUG
LOGGING_FORMAT = "%(levelname)s: %(asctime)s | [%(funcName)s() ln%(lineno)d] : %(message)s"

# Throw KeyError if these are not present
DB_HOST = environ["DB_HOST"]
DB_PORT = environ["DB_PORT"]
DB_NAME = environ["POSTGRES_DB"]
DB_USER = environ["POSTGRES_USER"]
DB_PASSWORD = environ["POSTGRES_PASSWORD"]


def get_session_maker() -> async_sessionmaker:
    engine = create_async_engine(url=f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
                                 pool_size=10,
                                 max_overflow=20,
                                 pool_timeout=30,
                                 echo=ENVIRONMENT == "DEV",
                                 pool_pre_ping=True)

    return async_sessionmaker(bind=engine,
                              class_=AsyncSession,
                              expire_on_commit=False)


API_PORT = int(environ.get("API_PORT", 8080))
API_HOST = environ.get("API_HOST", "0.0.0.0")

from fastapi import APIRouter

from api.v1.prices.router import router as prices_router
from api.v1.stations.router import router as stations_router
from api.v1.metrics.router import router as metrics_router
from api.v1.users.router import router as users_router
from api.v1.mpg.router import router as mpg_router
from api.v1.vehicles.router import router as vehicles_router
from api.v1.health.router import router as health_router


v1_router = APIRouter(prefix='/v1')
# Not yet implemented
v1_router.include_router(prices_router,
                         include_in_schema=False)
v1_router.include_router(stations_router,
                         include_in_schema=False)
v1_router.include_router(metrics_router,
                         include_in_schema=False)

# Implemented
v1_router.include_router(users_router)
v1_router.include_router(mpg_router)
v1_router.include_router(vehicles_router)
v1_router.include_router(health_router)

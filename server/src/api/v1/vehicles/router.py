from fastapi import APIRouter

from . import schemas, service
from api.core.schemas import ActionResponse, LIMIT, OFFSET
from api.core.deps.auth import USER_ID
from api.core.deps.database import DB_SESSION

router = APIRouter(prefix='/vehicles',
                   tags=['Vehicles'])


@router.get('', status_code=200)
async def get_vehicles(session: DB_SESSION,
                       user_id: USER_ID,
                       limit: LIMIT = 10,
                       offset: OFFSET = 0) -> list[schemas.Vehicle]:
    # List all vehicles that a user has linked to them, with pagination
    return await service.get_vehicles(session=session,
                                      user_id=user_id,
                                      limit=limit,
                                      offset=offset)


@router.get('/{registration}', status_code=200)
async def get_vehicle(session: DB_SESSION,
                      user_id: USER_ID,
                      registration: str) -> schemas.Vehicle:
    # Get user's vehicle based on registration
    return await service.get_vehicle(session=session,
                                     user_id=user_id,
                                     registration=registration.upper().replace(' ', ''))


@router.post('', status_code=201)
async def add_vehicle(session: DB_SESSION,
                      user_id: USER_ID,
                      vehicle: schemas.Vehicle) -> ActionResponse:
    # Add vehicle to user's ownership / Vehicles table if the Vehicle doesn't already exist in the table
    return await service.add_vehicle(session=session,
                                     vehicle=vehicle,
                                     user_id=user_id)

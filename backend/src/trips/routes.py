"""module for Trip Resource"""
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import TripService
from .schemas import TripCreateModel, TripResponseModel, StatusUpdateModel
from src.db.main import get_session
from uuid import UUID
from typing import List
from src.auth.dependency import AccessToken, RoleChecker
from fastapi.responses import JSONResponse


access = AccessToken()
trip_router = APIRouter(
    prefix='/api'
)

trip_service = TripService()


@trip_router.get('/trips', response_model=List[TripResponseModel])
async def get_trips(
    session: AsyncSession = Depends(get_session),
    token_detail: dict = Depends(access)
):
    trips = await trip_service.get_trips(session)
    return trips


@trip_router.get('/trips/{trip_id}', response_model=TripResponseModel)
async def get_a_trip(
    trip_id: str,
    session: AsyncSession = Depends(get_session),
    token_detail: dict = Depends(access)
):
    trip = await trip_service.get_a_trip(trip_id, session)
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="trip Not found"
        )

    return trip

@trip_router.post('/trips', response_model=TripResponseModel)
async def create_trip(
    trip_data: TripCreateModel,
    session: AsyncSession = Depends(get_session),
    token_detail: dict = Depends(access),
    role: bool = Depends(RoleChecker(['driver']))

):
    user_id = token_detail['user']['id']
    trip = await trip_service.create_trip(user_id, trip_data, session)
    return trip


@trip_router.patch('/trip/{trip_id}/status')
async def update_trip(
    trip_id: str,
    trip_data: StatusUpdateModel,
    session: AsyncSession = Depends(get_session),
    token_detail: dict = Depends(access),
    role: bool = Depends(RoleChecker(['driver']))

):
    trip = await trip_service.update_trip(trip_id, trip_data, session)
    return JSONResponse(
        content={
            "message": "trip status updated",
            "status": trip.status
        }
    )

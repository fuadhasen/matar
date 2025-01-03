"""module for Trip Resource"""
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import TripService
from .schema import TripCreateModel, TripResponseModel
from src.db.main import get_session
from uuid import UUID
from typing import List


trip_router = APIRouter(
    prefix='/api'
)

trip_service = TripService()


# Entire Trip
@trip_router.get('/trips', response_model=List[TripResponseModel])
async def get_trips(session: AsyncSession = Depends(get_session)):
    trips = await trip_service.get_trips(session)
    return trips

# get specific trip
@trip_router.get('/trips/{trip_id}', response_model=TripResponseModel)
async def get_a_trip(trip_id: str, session: AsyncSession = Depends(get_session)):
    trip = await trip_service.get_a_trip(trip_id, session)
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="trip Not found"
        )
    return trip


# create trip
@trip_router.post('/trip', response_model=TripResponseModel)
async def create_trip(
    trip_data: TripCreateModel,
    session: AsyncSession = Depends(get_session)
):
    trip = await trip_service.create_trip(trip_data, session)
    return trip


@trip_router.patch('/trip/{trip_id}/status')
async def update_trip(
    trip_id: str,
    trip_data: TripCreateModel,
    session: AsyncSession = Depends(get_session)
):
    trip = await trip_service.update_trip(trip_id, trip_data, session)
    return trip


# @trip_router.delete('/trip/{trip_id}')
# async def delete_trip(trip_id: str, session: AsyncSession = Depends(get_session)):
#     trip = await trip_service.delete_trip(trip_id, session)
#     return trip


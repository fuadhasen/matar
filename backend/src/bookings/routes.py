"""module for Booking Resource"""
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import BookingService
from .schemas import BookingCreateModel, BookingResponseModel
from src.db.main import get_session
from uuid import UUID
from typing import List
from src.auth.dependency import AccessToken, RoleChecker

access = AccessToken()


booking_router = APIRouter(
    prefix='/api'
)

booking_service = BookingService()


@booking_router.get('/bookings/{booking_id}', response_model=BookingResponseModel)
async def get_a_booking(
    booking_id: str,
    session: AsyncSession = Depends(get_session),
    token_detail: dict = Depends(access)
):
    booking = await booking_service.get_a_booking(booking_id, session)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="booking Not found"
        )
    return booking


@booking_router.post('/bookings', response_model=BookingResponseModel)
async def create_booking(
    booking_data: BookingCreateModel,
    session: AsyncSession = Depends(get_session),
    token_detail: dict = Depends(access),
    role: bool = Depends(RoleChecker(['tourist']))
):
    user_id = token_detail['user']['id']
    booking = await booking_service.create_booking(user_id, booking_data, session)
    return booking


@booking_router.delete('/bookings/{booking_id}')
async def delete_booking(
    booking_id: str,
    session: AsyncSession = Depends(get_session),
    token_detail: dict = Depends(access),
    role: bool = Depends(RoleChecker(['tourist']))
):
    user_id = token_detail['user']['id']
    booking = await booking_service.delete_booking(user_id, booking_id, session)
    return booking

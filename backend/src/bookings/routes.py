"""module for Booking Resource"""
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import BookingService
from .schema import BookingCreateModel, BookingResponseModel
from src.db.main import get_session
from uuid import UUID
from typing import List


booking_router = APIRouter()
booking_service = BookingService()


@booking_router.get('/bookings', response_model=List[BookingResponseModel])
async def get_booking(session: AsyncSession = Depends(get_session)):
    bookings = await booking_service.get_bookings(session)
    return bookings


@booking_router.get('/booking/{booking_id}', response_model=BookingResponseModel)
async def get_a_booking(booking_id: str, session: AsyncSession = Depends(get_session)):
    booking = await booking_service.get_a_booking(booking_id, session)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="booking Not found"
        )
    return booking


@booking_router.post('/booking', response_model=BookingResponseModel)
async def create_booking(
    booking_data: BookingCreateModel,
    session: AsyncSession = Depends(get_session)
):
    booking = await booking_service.create_booking(booking_data, session)
    return booking


@booking_router.patch('/booking/{booking_id}')
async def update_booking(
    booking_id: str,
    booking_data: BookingCreateModel,
    session: AsyncSession = Depends(get_session)
):
    booking = await booking_service.update_booking(booking_id, booking_data, session)
    return booking


@booking_router.delete('/booking/{booking_id}')
async def delete_booking(booking_id: str, session: AsyncSession = Depends(get_session)):
    booking = await booking_service.delete_booking(booking_id, session)
    return booking

"""module for Booking Resource"""

from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from .services import BookingService
from .schemas import BookingCreateModel, BookingResponseModel
from src.db.main import get_session
from uuid import UUID
from src.users.oauth import verify_is_tourist


router = APIRouter(prefix="/api", tags=["Bookings"])

booking_service = BookingService()


@router.post(
    "/bookings",
    response_model=BookingResponseModel,
    summary="Book a service",
    status_code=status.HTTP_201_CREATED,
)
async def book_a_service(
    booking: BookingCreateModel,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(verify_is_tourist),
):
    user_id = current_user.id
    booking.booking_date = booking.booking_date.replace(tzinfo=None)
    booking_data = {**booking.model_dump(), "user_id": user_id}
    return await booking_service.book_a_service(
        booking_data=booking_data,
        session=session,
    )


@router.put(
    "/bookings/{booking_id}",
    response_model=BookingResponseModel,
    summary="Update a booking",
)
async def update_a_service(
    booking_id: UUID,
    booking: BookingCreateModel,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(verify_is_tourist),
):
    booking_data = {**booking.model_dump(exclude_none=True)}
    return await booking_service.update_a_service(
        session=session,
        booking_id=booking_id,
        booking_data=booking_data,
    )


@router.delete(
    "/bookings/{booking_id}",
    summary="Delete a booking",
)
async def delete_a_service(
    booking_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(verify_is_tourist),
):
    return await booking_service.delete_a_service(session, booking_id)

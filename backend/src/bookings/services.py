"""module for Booking Service"""

from fastapi import status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import Booking
from sqlmodel import select

from fastapi.exceptions import HTTPException
from uuid import UUID


class BookingService:
    """class for Booking service methods"""

    async def book_a_service(
        self,
        booking_data: dict,
        session: AsyncSession,
    ):
        try:

            new_booking = Booking(**booking_data)
            session.add(new_booking)
            await session.commit()
            return new_booking
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid data service_id",
            )

    async def update_a_service(
        self,
        booking_id: UUID,
        booking_data: dict,
        session: AsyncSession,
    ):
        try:
            statement = select(Booking).where(Booking.id == booking_id)
            res = await session.exec(statement)
            booking = res.first()
            if booking is None:
                return None
            for key, value in booking_data.items():
                setattr(booking, key, value)
            await session.commit()
            return booking
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid data service_id",
            )

    async def delete_a_service(
        self,
        booking_id: UUID,
        session: AsyncSession,
    ):
        statement = select(Booking).where(Booking.id == booking_id)
        res = await session.exec(statement)
        booking = res.first()
        if booking is None:
            return None
        session.delete(booking)
        await session.commit()
        return booking

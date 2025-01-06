"""module for Booking Service"""
from fastapi import status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy import desc
from src.db.models import Booking
from fastapi.exceptions import HTTPException
from .schema import BookingCreateModel
from uuid import UUID
from datetime import datetime
from src.trips.routes import trip_service
from src.drivers.routes import driver_service


class BookingService:
    """class for Booking service methods"""
    async def get_bookings(self, session: AsyncSession):
        statement = select(Booking).order_by(desc(Booking.created_at))
        res = await session.exec(statement)
        result = res.all()
        return result

    async def get_a_booking(self, booking_id: str, session: AsyncSession):
        statement = select(Booking).where(Booking.id == booking_id)
        res = await session.exec(statement)
        result = res.first()
        return result if result is not None else None

    async def create_booking(self, user_id, booking_data: BookingCreateModel, session: AsyncSession):
        trip_id = booking_data.trip_id
        if (trip_service.get_a_trip(trip_id, session) is None):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="trip with this id is not found"
                            )

        driver_id = booking_data.driver_id
        if (driver_service.get_a_driver(driver_id, session) is  None):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="driver with this id is not found"
                            )
    
        new_data = booking_data.model_dump()

        new_booking = Booking(**new_data)
        new_booking.booking_date = datetime.strptime(new_data['booking_date'],
                                                     "%Y-%m-%d")
        new_booking.driver_id = UUID(new_data['driver_id'])
        new_booking.trip_id = UUID(new_data['trip_id'])

        new_booking.user_id = user_id
        session.add(new_booking)
        await session.commit()
        return new_booking

    async def update_booking(self, booking_id: str, booking_data: BookingCreateModel, session: AsyncSession):
        trip_id = booking_data.trip_id
        trip = await trip_service.get_a_trip(trip_id, session)
        if not trip:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="trip with this id is not found"
                            )

        driver_id = booking_data.driver_id
        driver = await driver_service.get_a_driver(driver_id, session)
        if not driver:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="driver with this id is not found"
                            )

        booking = await self.get_a_booking(booking_id, session)
        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found"
            )

        lists = ['driver_id', 'trip_id', 'booking_date']
        new_data = booking_data.model_dump()
        booking.booking_date = datetime.strptime(new_data['booking_date'],
                                                     "%Y-%m-%d")        
        booking.driver_id = UUID(new_data['driver_id'])
        booking.trip_id = UUID(new_data['trip_id'])
        for k, v in new_data.items():
            if k not in lists:
                setattr(booking, k, v)
        await session.commit()
        await session.refresh(booking)
        return booking

    async def delete_booking(self, user_id,  booking_id: str, session: AsyncSession):
        statement = select(Booking).where(Booking.user_id == user_id)
        res = await session.exec(statement)
        bking = res.first()
        if not bking:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not allowed to delete others booking"
            )

        booking = await self.get_a_booking(booking_id, session)
        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking Not found"
            )

        await session.delete(booking)
        await session.commit()
        return {}

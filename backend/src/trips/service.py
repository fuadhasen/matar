"""module for Trip Service"""

from fastapi import status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy import desc

# from src.db.models import Trip
from fastapi.exceptions import HTTPException
from .schemas import TripCreateModel
from uuid import UUID
from datetime import datetime
from src.db.models import Driver


class TripService:
    pass
    """class for Trip services"""

    async def get_trips(self, session: AsyncSession):
        statement = select(Trip).order_by(desc(Trip.created_at))
        res = await session.exec(statement)
        result = res.all()
        return result

    async def get_a_trip(self, trip_id: str, session: AsyncSession):
        statement = select(Trip).where(Trip.id == trip_id)
        res = await session.exec(statement)
        result = res.first()
        return result if result is not None else None

    async def create_trip(
        self, user_id, trip_data: TripCreateModel, session: AsyncSession
    ):
        statement = select(Driver).where(Driver.user_id == user_id)
        res = await session.exec(statement)
        driver = res.first()
        if not driver:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="driver not created for this user",
            )

        new_data = trip_data.model_dump()
        new_trip = Trip(**new_data)
        new_trip.driver_id = driver.id
        new_trip.trip_date = datetime.strptime(new_data["trip_date"], "%Y-%m-%d")
        session.add(new_trip)
        await session.commit()
        return new_trip

    async def update_trip(
        self, trip_id: str, trip_data: TripCreateModel, session: AsyncSession
    ):
        trip = await self.get_a_trip(trip_id, session)
        if not trip:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tripe with this id Not found",
            )

        new_data = trip_data.model_dump()
        for k, v in new_data.items():
            setattr(trip, k, v)

        await session.commit()
        return trip

    async def delete_trip(self, trip_id: str, session: AsyncSession):
        trip = await self.get_a_trip(trip_id, session)
        if not trip:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
            )

        await session.delete(trip)
        await session.commit()
        return {}

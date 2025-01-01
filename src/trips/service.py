"""module for Trip Service"""
from fastapi import status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy import desc
from src.db.models import Trip
from fastapi.exceptions import HTTPException
from .schema import TripCreateModel
from uuid import UUID
from datetime import datetime


class TripService:
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

    async def create_trip(self, trip_data: TripCreateModel, session: AsyncSession):
        new_data = trip_data.model_dump()

        new_trip = Trip(**new_data)
        new_trip.trip_date = datetime.strptime(new_data['trip_date'], "%Y-%m-%d")
        session.add(new_trip)
        await session.commit()
        return new_trip

    async def update_trip(self, trip_id: str, trip_data: TripCreateModel, session: AsyncSession):
        trip = await self.get_a_trip(trip_id, session)
        if not trip:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found"
            )

        new_data = trip_data.model_dump()
        trip.trip_date = datetime.strptime(new_data['trip_date'], "%Y-%m-%d")

        for k, v in new_data.items():
            if (k != 'trip_date'):
                setattr(trip, k, v)
        session.add(trip)
        await session.commit()
        return trip

    async def delete_trip(self, trip_id: str, session: AsyncSession):
        trip = await self.get_a_trip(trip_id, session)
        if not trip:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found"
            )

        await session.delete(trip)
        await session.commit()
        return {}


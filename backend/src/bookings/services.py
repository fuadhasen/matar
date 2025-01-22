"""module for Booking Service"""

from fastapi import status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy import desc
from src.db.models import Booking
from fastapi.exceptions import HTTPException
from .schemas import BookingCreateModel
from uuid import UUID
from datetime import datetime
from src.services.routes import driver_service


class BookingService:
    """class for Booking service methods"""

    async def get_tourist_bookings(self, tourist_id: UUID, session: AsyncSession):
        statement = select(Booking).where(Booking.tourist_id == tourist_id)
        res = await session.exec(statement)
        result = res.all()
        return result

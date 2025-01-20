"""module for Driver Service"""

from fastapi import status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy import desc
from src.db.models import Airport
from fastapi.exceptions import HTTPException
from .schemas import AirportCreateModel, AirportUpdateModel
from uuid import UUID


class AirportService:
    """class for Airport services"""

    async def get_airports(self, session: AsyncSession):
        statement = select(Airport).order_by(desc(Airport.created_at))
        res = await session.exec(statement)
        result = res.all()
        return result

    async def get_an_airport(self, airport_id: str, session: AsyncSession):
        statement = select(Airport).where(Airport.id == airport_id)
        res = await session.exec(statement)
        result = res.first()
        return result if result is not None else None

    async def create_airport(
        self, airport_data: AirportCreateModel, session: AsyncSession
    ):
        statement = select(Airport).where(Airport.name == airport_data.name)
        res = await session.exec(statement)
        airport = res.first()
        if airport:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="airport with this name already exist",
            )

        new_data = airport_data.model_dump()

        new_airport = Airport(**new_data)
        session.add(new_airport)
        await session.commit()
        return new_airport

    async def update_airport(
        self, airport_id: str, airport_data: AirportUpdateModel, session: AsyncSession
    ):
        airport = await self.get_an_airport(airport_id, session)
        if not airport:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found",
            )

        airport.name = airport_data.name
        await session.commit()
        return airport

    async def delete_airport(self, airport_id: str, session: AsyncSession):
        airport = await self.get_an_airport(airport_id, session)
        if not airport:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found",
            )

        session.delete(airport)
        await session.commit()
        return airport

    async def get_airport_by_name(self, airport_name: str, session: AsyncSession):
        statement = select(Airport).where(Airport.name == airport_name)
        res = await session.exec(statement)
        result = res.first()
        return result if result is not None else None

    async def get_airport_services(self, airport_id: str, session: AsyncSession):
        statement = select(Airport).where(Airport.id == airport_id)
        res = await session.exec(statement)
        result = res.first()
        return result.services if result is not None else None

    async def search_airports(self, search_term: str, session: AsyncSession):
        statement = select(Airport).where(Airport.name.ilike(f"%{search_term}%"))
        res = await session.exec(statement)
        result = res.all()
        return result

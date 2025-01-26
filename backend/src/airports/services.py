"""module for Driver Service"""

from fastapi import status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy import desc
from src.db.models import Airport
from fastapi.exceptions import HTTPException
from .schemas import AirportCreateModel, AirportUpdateModel


class AirportService:
    """class for Airport services"""

    async def get_airports(self, session: AsyncSession):
        """get all airports"""
        statement = select(Airport).order_by(desc(Airport.created_at))
        res = await session.exec(statement)
        result = res.all()
        return result

    async def get_an_airport(self, airport_id: str, session: AsyncSession):
        """get an airport"""
        statement = select(Airport).where(Airport.id == airport_id)
        res = await session.exec(statement)
        result = res.first()
        return result if result is not None else None

    async def create_airport(
        self, airport_data: AirportCreateModel, session: AsyncSession
    ):
        """create an airport"""
        statement = select(Airport).where(
            Airport.airport_name == airport_data.airport_name
        )
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

    async def search_airports(self, search_term: str, session: AsyncSession):
        """search airports by name or location"""
        statement = select(Airport).where(
            (Airport.airport_name.ilike(f"%{search_term}%"))
            | (Airport.airport_location.ilike(f"%{search_term}%"))
        )
        res = await session.exec(statement)
        result = res.all()
        return result

    async def update_airport(
        self, airport_id: str, airport_data: AirportUpdateModel, session: AsyncSession
    ):
        """update an airport"""
        airport = await self.get_an_airport(airport_id, session)
        if not airport:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found",
            )
        airport_data = airport_data.model_dump(exclude_none=True)
        for key, value in airport_data.items():
            setattr(airport, key, value)
        await session.commit()
        return airport

    async def delete_airport(self, airport_id: str, session: AsyncSession):
        """delete an airport"""
        airport = await self.get_an_airport(airport_id, session)
        if not airport:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found",
            )
        await session.delete(airport)
        await session.commit()

    async def get_airport_by_name(self, airport_name: str, session: AsyncSession):
        """get an airport by name"""
        statement = select(Airport).where(Airport.name == airport_name)
        res = await session.exec(statement)
        result = res.first()
        return result if result is not None else None

    async def get_airport_services(self, airport_id: str, session: AsyncSession):
        """get an airport services"""
        statement = select(Airport).where(Airport.id == airport_id)
        res = await session.exec(statement)
        result = res.first()
        return result.services if result is not None else None

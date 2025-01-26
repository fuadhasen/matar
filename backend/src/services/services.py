"""module for Driver Service"""

from fastapi import HTTPException, status
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from src.db.models import Service


class DriverService:
    """class for Driver services"""

    async def create_a_service(
        self,
        session: AsyncSession,
        service_data: dict,
    ):
        """create a service"""
        try:
            service = Service(**service_data)
            session.add(service)
            await session.commit()
            return service
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid airport_id",
            )

    async def update_a_service(
        self,
        session: AsyncSession,
        service_id: UUID,
        service_data: dict,
    ):
        """update a service"""
        try:
            statement = select(Service).where(Service.id == service_id)
            res = await session.exec(statement)
            service = res.first()
            if service is None:
                return None
            for key, value in service_data.items():
                setattr(service, key, value)
            await session.commit()
            return service
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid airport_id",
            )

    async def delete_a_service(
        self,
        session: AsyncSession,
        service_id: UUID,
    ):
        """delete a service"""
        statement = select(Service).where(Service.id == service_id)
        res = await session.exec(statement)
        service = res.first()
        if service is None:
            return None
        await session.delete(service)
        await session.commit()
        return service

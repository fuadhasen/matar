"""module for Driver Service"""
from fastapi import status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy import desc
from src.db.models import Driver
from fastapi.exceptions import HTTPException
from .schema import DriverCreateModel
from uuid import UUID


class DriverService:
    """class for Driver services"""
    async def get_drivers(self, session: AsyncSession):
        statement = select(Driver).order_by(desc(Driver.created_at))
        res = await session.exec(statement)
        result = res.all()
        return result

    async def get_a_driver(self, driver_id: str, session: AsyncSession):
        statement = select(Driver).where(Driver.id == driver_id)
        res = await session.exec(statement)
        result = res.first()
        return result if result is not None else None

    async def find_by_registration_num(self, driver_registration_no: str, session: AsyncSession):
        statement = select(Driver).where(Driver.vehicle_registration_number == driver_registration_no)
        res = await session.exec(statement)
        return res.first()

    async def create_driver(self, driver_data: DriverCreateModel, session: AsyncSession):
        driver_registration_num = driver_data.vehicle_registration_number
        driver = await self.find_by_registration_num(driver_registration_num, session)
        if driver:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="driver with this registration number already exist"
            )
        new_data = driver_data.model_dump()

        new_driver = Driver(**new_data)
        session.add(new_driver)
        await session.commit()
        return new_driver

    async def update_driver(self, driver_id: str, driver_data: DriverCreateModel, session: AsyncSession):
        driver = await self.get_a_driver(driver_id, session)
        if not driver:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found"
            )

        new_data = driver_data.model_dump()
        for k, v in new_data.items():
            setattr(driver, k, v)
        return driver

    async def delete_driver(self, driver_id: str, session: AsyncSession):
        driver = await self.get_a_driver(driver_id, session)
        if not driver:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found"
            )

        await session.delete(driver)
        await session.commit()
        return {}


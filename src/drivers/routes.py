"""module for Drivers Resource"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from .service import DriverService
from .schema import DriverCreateModel, DriverResponseModel
from src.db.main import get_session
from uuid import UUID
from typing import List


driver_router = APIRouter()
driver_service = DriverService()


@driver_router.get('/drivers', response_model=List[DriverResponseModel])
async def get_driver(session: AsyncSession = Depends(get_session)):
    drivers = await driver_service.get_drivers(session)
    return drivers


@driver_router.get('/driver/{driver_id}', response_model=DriverResponseModel)
async def get_a_driver(driver_id: UUID, session: AsyncSession = Depends(get_session)):
    driver = await driver_service.get_a_driver(driver_id, session)
    return driver


@driver_router.post('/driver')
async def create_driver(
    driver_data: DriverCreateModel,
    session: AsyncSession = Depends(get_session)
):
    driver = await driver_service.create_driver(driver_data, session)
    return driver


@driver_router.patch('/driver/{driver_id}', response_model=DriverModel)
async def update_driver(
    driver_id: UUID,
    driver_data: DriverCreateModel,
    session: AsyncSession = Depends(get_session)
):
    driver = await driver_service.update_driver(driver_id, driver_data, session)
    return driver


@driver_router.delete('/driver/{driver_id}')
async def delete_driver(driver_id: UUID, session: AsyncSession = Depends(get_session)):
    driver = await driver_service.delete_driver(driver_id, session)
    return driver

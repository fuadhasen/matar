"""module for Drivers Resource"""
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import DriverService
from .schema import DriverCreateModel, DriverResponseModel
from src.db.main import get_session
from uuid import UUID
from typing import List


driver_router = APIRouter(
    prefix='/api'
)

driver_service = DriverService()


@driver_router.get('/drivers', response_model=List[DriverResponseModel])
async def get_driver(session: AsyncSession = Depends(get_session)):
    drivers = await driver_service.get_drivers(session)
    return drivers


@driver_router.get('/driver/{driver_id}', response_model=DriverResponseModel)
async def get_a_driver(driver_id: str, session: AsyncSession = Depends(get_session)):
    driver = await driver_service.get_a_driver(driver_id, session)
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="driver Not found"
        )
    return driver


# create driver
@driver_router.post('/drivers/register', response_model=DriverResponseModel)
async def create_driver(
    driver_data: DriverCreateModel,
    session: AsyncSession = Depends(get_session)
):
    driver = await driver_service.create_driver(driver_data, session)
    return driver


# wait this from admin.
@driver_router.get('/driver/{driver_id}/verify', response_model=DriverResponseModel)
async def get_a_driver(driver_id: str, session: AsyncSession = Depends(get_session)):
    driver = await driver_service.get_a_driver(driver_id, session)
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="driver Not found"
        )
    return driver


# @driver_router.patch('/driver/{driver_id}')
# async def update_driver(
#     driver_id: str,
#     driver_data: DriverCreateModel,
#     session: AsyncSession = Depends(get_session)
# ):
#     driver = await driver_service.update_driver(driver_id, driver_data, session)
#     return driver


# @driver_router.delete('/driver/{driver_id}')
# async def delete_driver(driver_id: str, session: AsyncSession = Depends(get_session)):
#     driver = await driver_service.delete_driver(driver_id, session)
#     return driver

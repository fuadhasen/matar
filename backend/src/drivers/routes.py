"""module for Drivers Resource"""
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import DriverService
from .schema import DriverCreateModel, DriverResponseModel
from src.db.main import get_session
from uuid import UUID
from typing import List
from src.auth.dependency import AccessToken
from src.auth.routes import user_service


driver_router = APIRouter(
    prefix='/api'
)

driver_service = DriverService()
access = AccessToken()


@driver_router.get('/drivers', response_model=List[DriverResponseModel])
async def get_driver(session: AsyncSession = Depends(get_session)):
    drivers = await driver_service.get_drivers(session)
    return drivers


@driver_router.get('/drivers/{driver_id}', response_model=DriverResponseModel)
async def get_a_driver(driver_id: str, session: AsyncSession = Depends(get_session)):
    driver = await driver_service.get_a_driver(driver_id, session)
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="driver Not found"
        )
    return driver


@driver_router.post('/drivers/register', response_model=DriverResponseModel)
async def create_driver(
    driver_data: DriverCreateModel,
    session: AsyncSession = Depends(get_session),
    token_detail: dict = Depends(access)
):
    user_email = token_detail['user']['user_email']
    user = await user_service.get_auser_byemail(user_email, session)
    if user.role != 'driver':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="user with driver role only can register here"
                        )
    driver = await driver_service.create_driver(user.id, driver_data, session)
    return driver


# role based access only for admins.
@driver_router.get('/drivers/{driver_id}/verify', response_model=DriverResponseModel)
async def check_status(
    driver_id: str,
    session: AsyncSession = Depends(get_session),
    token_detail: dict = Depends(access)
):
    driver = await driver_service.get_a_driver(driver_id, session)
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="driver Not found"
        )

    return JSONResponse(
        content={
           "verified" : driver.verified
        }
    )


# role based access only for admins.
@driver_router.patch('/drivers/{driver_id}/verify', response_model=DriverResponseModel)
async def verify_status(
    driver_id: str,
    session: AsyncSession = Depends(get_session),
    token_detail: dict = Depends(access)
):
    driver = await driver_service.get_a_driver(driver_id, session)
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="driver Not found"
        )

    driver.verified = True
    await session.commit()
    return JSONResponse(
        content={
            "message": "Driver verified successfully",
            "verified" : driver.verified
        }
    )


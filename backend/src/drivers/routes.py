"""module for Drivers Resource"""
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import DriverService
from .schema import DriverCreateModel, DriverResponseModel, VerifyModel
from src.db.main import get_session
from uuid import UUID
from typing import List
from src.auth.dependency import AccessToken
from src.auth.service import UserService
from src.auth.dependency import RoleChecker


user_service = UserService()
driver_router = APIRouter(
    prefix='/api'
)

driver_service = DriverService()
access = AccessToken()


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


@driver_router.get('/drivers/{driver_id}/verify', response_model=DriverResponseModel)
async def check_status(
    driver_id: str,
    session: AsyncSession = Depends(get_session),
    token_detail: dict = Depends(access),
    role: bool = Depends(RoleChecker(['staffs']))
):
    driver = await driver_service.get_a_driver(driver_id, session)
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="driver Not found"
        )

    return driver


@driver_router.patch('/drivers/{driver_id}/verify')
async def verify_driver(
    driver_id: str,
    driver_data: VerifyModel,
    session: AsyncSession = Depends(get_session),
    token_detail: dict = Depends(access),
    role: bool = Depends(RoleChecker(['staff']))
):
    driver = await driver_service.update_driver(driver_id, driver_data, session)

    return JSONResponse(
        content={
            'verified': driver.verified
        }
    )


"""Authentication and user management routes."""

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .services import UserService
from .schemas import (
    UserCreateModel,
    DriverCreateModel,
    TouristCreateModel,
    UserResponseModel,
    DriverResponseModel,
    TouristResponseModel,
    DisableModel,
    VerifyDriverModel,
)
from .dependency import AccessToken

router = APIRouter(prefix="/api", tags=["Users"])
user_service = UserService()
access_token = AccessToken()


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponseModel,
)
async def register_user(
    user_data: UserCreateModel,
    session: AsyncSession = Depends(get_session),
):
    """Register a new user."""
    try:
        user = await user_service.register_user(user_data, session)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return user


@router.put("/update")
async def update_me(
    user_data: UserCreateModel,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(access_token),
):
    """Update the current user."""
    try:
        await user_service.update_user(current_user, user_data, session)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return {"message": "User updated successfully"}


@router.post("/register/driver", status_code=status.HTTP_201_CREATED)
async def register_driver(
    driver_data: DriverCreateModel,
    session: AsyncSession = Depends(get_session),
):
    """Register a new driver."""
    try:
        driver = await user_service.register_driver(driver_data, session)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return driver


@router.post("/register/tourist", status_code=status.HTTP_201_CREATED)
async def register_tourist(
    tourist_data: TouristCreateModel,
    session: AsyncSession = Depends(get_session),
):
    """Register a new tourist."""
    try:
        tourist = await user_service.register_tourist(tourist_data, session)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return tourist


@router.put("/driver/verify", status_code=status.HTTP_200_OK)
async def verify_driver(
    driver_data: VerifyDriverModel,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(access_token),
):
    """Verify a driver."""
    try:
        await user_service.verify_driver(driver_data, session)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return {"message": "Driver verified successfully"}


@router.get("/users", status_code=status.HTTP_200_OK)
async def get_users(
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(access_token),
):
    """Get all users."""
    try:
        users = await user_service.get_users(session)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return users

"""Authentication and user management routes."""

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession
from pydantic import EmailStr
from uuid import UUID
from src.db.main import get_session
from .services import UserService
from .schemas import (
    UserCreateModel,
    DriverCreateModel,
    TouristCreateModel,
    UserResponseModel,
    DriverResponseModel,
    TouristResponseModel,
    Token,
)
from src.users.oauth import get_current_user, verify_is_staff

router = APIRouter(prefix="/api", tags=["Users"])
user_service = UserService()


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponseModel,
    summary="Register a new staff user",
)
async def register_user(
    user_data: UserCreateModel,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(verify_is_staff),
):
    """Register a new user."""
    try:
        user = await user_service.register_user(user_data, session)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return user


@router.put(
    "/update",
    status_code=status.HTTP_200_OK,
    response_model=UserResponseModel,
    summary="Update the current user",
)
async def update_me(
    user_data: UserCreateModel,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    """Update the current user."""
    try:
        user = await user_service.update_user(user_data, current_user, session)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return user


@router.post(
    "/register/driver",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponseModel,
    summary="Register a new driver",
)
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


@router.post(
    "/register/tourist",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponseModel,
    summary="Register a new tourist",
)
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


@router.put(
    "/driver/{driver_email}/verify",
    status_code=status.HTTP_200_OK,
    summary="Verify a driver",
)
async def verify_driver(
    driver_email: EmailStr,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(verify_is_staff),
):
    """Verify a driver."""
    try:
        await user_service.verify_driver(driver_email, session)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return {"message": "Driver verified successfully"}


@router.put(
    "/user/{user_id}/disable",
    status_code=status.HTTP_200_OK,
    summary="Disable a user",
)
async def disable_driver(
    user_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(verify_is_staff),
):
    """Disable a driver."""
    try:
        await user_service.disable_user(user_id, session)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return {"message": "Driver disabled successfully"}


@router.get(
    "/users",
    status_code=status.HTTP_200_OK,
    response_model=list[UserResponseModel],
    summary="Get all users",
)
async def get_users(
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(verify_is_staff),
):
    """Get all users."""
    try:
        users = await user_service.get_users(session)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return users


@router.get(
    "/drivers",
    status_code=status.HTTP_200_OK,
    response_model=list[DriverResponseModel],
    summary="Get all drivers",
)
async def get_drivers(
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(verify_is_staff),
):
    """Get all drivers."""
    try:
        users = await user_service.get_drivers(session)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return users


@router.get(
    "/tourists",
    status_code=status.HTTP_200_OK,
    response_model=list[TouristResponseModel],
    summary="Get all tourists",
)
async def get_tourists(
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(verify_is_staff),
):
    """Get all tourists."""
    try:
        users = await user_service.get_tourists(session)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return users


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=Token,
    summary="Create a token",
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    """Login a user."""
    try:
        token = await user_service.login(form_data, session)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return token


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=UserResponseModel,
    summary="Get the current user",
)
async def get_me(
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    """Get the current user."""
    try:
        user = await user_service.get_me(current_user, session)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return user

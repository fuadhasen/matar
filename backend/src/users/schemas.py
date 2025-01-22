"""Pydantic validation"""

from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional, List
from src.db.models import RoleEnum
from src.services.schemas import ServiceCreateModel
from src.bookings.schemas import BookingResponseModel


class UserCreateModel(BaseModel):
    """User create model"""

    first_name: str
    last_name: str
    email: str
    password: str
    phone_number: Optional[str]
    role: RoleEnum = RoleEnum.staff
    verified: bool = False
    is_active: bool = True


class DriverCreateModel(UserCreateModel):
    """Driver create model"""

    role: RoleEnum = RoleEnum.driver
    languages_spoken: Optional[str]
    experience_years: Optional[int]
    services: Optional[List[ServiceCreateModel]] = []


class TouristCreateModel(UserCreateModel):
    """Tourist create model"""

    role: RoleEnum = RoleEnum.tourist
    bookings: Optional[List[BookingResponseModel]] = []


class UserResponseModel(BaseModel):
    """User response model"""

    id: UUID
    first_name: str
    last_name: str
    email: str
    password: str
    phone_number: Optional[str]
    role: RoleEnum
    is_active: bool
    verified: bool
    created_at: datetime


class TouristResponseModel(UserResponseModel):
    """Tourist response model"""

    bookings: Optional[List[BookingResponseModel]] = []


class DriverResponseModel(UserResponseModel):
    """Driver response model"""

    languages_spoken: Optional[str]
    experience_years: Optional[int]
    services: Optional[List[ServiceCreateModel]] = []


class DisableModel(BaseModel):
    """Disable model"""

    is_active: bool


class LoginModel(BaseModel):
    """Login model"""

    email: EmailStr
    password: str

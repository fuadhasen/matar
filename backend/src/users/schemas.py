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
    email: EmailStr
    password: str
    phone_number: Optional[str]


class UserUpdateModel(BaseModel):
    """User update model"""

    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    phone_number: Optional[str]


class DriverCreateModel(UserCreateModel):
    """Driver create model"""

    languages_spoken: Optional[str]
    experience_years: Optional[int]
    services: Optional[List[ServiceCreateModel]] = []


class TouristCreateModel(UserCreateModel):
    """Tourist create model"""

    bookings: Optional[List[BookingResponseModel]] = []


class UserResponseModel(BaseModel):
    """User response model"""

    id: UUID
    first_name: str
    last_name: str
    email: str
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


class VerifyDriverModel(BaseModel):
    """Verify driver model"""

    verified: bool


class CredentialsModel(BaseModel):
    """Login model"""

    username: EmailStr
    password: str


class Token(BaseModel):
    """Token model"""

    access_token: str
    token_type: str


class DataToken(BaseModel):
    """Data token model"""

    email: Optional[EmailStr] = None

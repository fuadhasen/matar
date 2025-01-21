"""Pydantic validation"""

from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from sqlmodel import Field
from typing import Optional, List
from src.db.models import RoleEnum
from src.drivers.schemas import ServiceCreateModel


class UserCreateModel(BaseModel):
    first_name: str = Field(max_length=20)
    last_name: str = Field(max_length=20)
    email: EmailStr
    phone_number: Optional[str]
    password: str
    phone_number: str
    role: RoleEnum = RoleEnum.tourist
    is_active: bool = Field(default="true")


class DriverCreateModel(UserCreateModel):
    role: RoleEnum = RoleEnum.driver
    languages_spoken: Optional[str]
    experience_years: Optional[int]
    verified: bool
    services: List[ServiceCreateModel]


class AdminCreateModel(UserCreateModel):
    role: RoleEnum = RoleEnum.admin


class UserResponseModel(BaseModel):
    id: UUID
    created_at: datetime
    first_name: str = Field(max_length=20)
    last_name: str = Field(max_length=20)
    email: EmailStr
    phone_number: str
    role: RoleEnum
    is_active: bool


class LoginModel(BaseModel):
    email: EmailStr
    password: str


class DisableModel(BaseModel):
    is_active: str

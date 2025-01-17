"""Pydantic validation"""

from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from sqlmodel import Field
from src.db.models import RoleEnum
from typing import Optional


class UserCreateModel(BaseModel):
    first_name: str = Field(max_length=20)
    last_name: str = Field(max_length=20)
    email: EmailStr
    password: Optional[str]
    phone_number: str
    role: RoleEnum
    is_active: bool = Field(default="true")


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

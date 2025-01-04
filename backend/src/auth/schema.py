"""Pydantic validation"""
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from sqlmodel import Field
from src.db.models import RoleEnum
from typing import Optional


class UserCreateModel(BaseModel):
    full_name: str = Field(max_length=20)
    email: str
    password: Optional[str]
    phone_number: str
    role: RoleEnum
    is_active: str = Field(default=True)


class UserResponseModel(BaseModel):
    id: UUID
    created_at: datetime
    full_name: str = Field(max_length=20)
    email: str
    phone_number: str
    role: RoleEnum
    is_active: bool


class LoginModel(BaseModel):
    email: str
    password: str


class DisableModel(BaseModel):
    is_active: str
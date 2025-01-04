"""module for pydantic validation"""
from pydantic import BaseModel
from sqlmodel import Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class DriverCreateModel(BaseModel):
    vehicle_type: str = Field(max_length=50)
    vehicle_registration_number: str = Field(max_length=50, unique=True)
    languages_spoken: Optional[str] = Field(max_length=255)
    experience_years: Optional[int] = Field(default=0)
    verified: bool = Field(default=False)

    class Config:
        orm_mode: True

class DriverResponseModel(DriverCreateModel):
    id: UUID
    created_at: datetime

class VerifyModel(BaseModel):
    is_verified: bool
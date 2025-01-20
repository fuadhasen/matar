"""module for pydantic validation"""

from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime


class ServiceCreateModel(BaseModel):
    driver_id: UUID
    vehicle_model: Optional[str]
    vehicle_type: Optional[str]
    vehicle_color: Optional[str]
    vehicle_plate_number: Optional[str]
    capacity: Optional[int]


class ServiceResponseModel(ServiceCreateModel):
    id: UUID
    created_at: datetime


class DriverCreateModel(BaseModel):
    user_id: UUID
    languages_spoken: Optional[str]
    experience_years: Optional[int]
    verified: bool
    services: List[ServiceCreateModel]


class DriverResponseModel(DriverCreateModel):
    id: UUID
    created_at: datetime


class VerifyModel(BaseModel):
    verified: bool

"""module for pydantic validation"""

from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime


class ServiceCreateModel(BaseModel):
    vehicle_type: str
    vehicle_registration_number: str
    vehicle_model: str
    vehicle_color: str
    vehicle_capacity: int
    airport_id: UUID


class ServiceUpdateModel(BaseModel):
    vehicle_type: Optional[str] = None
    vehicle_registration_number: Optional[str] = None
    vehicle_model: Optional[str] = None
    vehicle_color: Optional[str] = None
    vehicle_capacity: Optional[int] = None
    airport_id: Optional[UUID] = None


class ServiceResponseModel(ServiceCreateModel):
    id: UUID
    available: bool = True
    created_at: datetime

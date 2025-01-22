"""module for pydantic validation"""

from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime


class ServiceCreateModel(BaseModel):
    vehicle_model: Optional[str]
    vehicle_type: Optional[str]
    vehicle_color: Optional[str]
    vehicle_plate_number: Optional[str]
    capacity: Optional[int]


class ServiceResponseModel(ServiceCreateModel):
    id: UUID
    available: bool = True
    created_at: datetime

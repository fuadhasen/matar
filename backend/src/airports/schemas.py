"""module for pydantic validation"""

from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from src.drivers.schemas import ServiceResponseModel


class AirportCreateModel(BaseModel):
    airport_name: str
    airport_location: str


class AirportResponseModel(AirportCreateModel):
    id: UUID
    created_at: datetime
    services: Optional[List[ServiceResponseModel]] = []


class AirportUpdateModel(BaseModel):
    airport_name: Optional[str]
    airport_location: Optional[str]

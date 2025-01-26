"""module for pydantic validation"""

from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from src.services.schemas import ServiceResponseModel


class AirportCreateModel(BaseModel):
    airport_name: str
    airport_location: str
    services: Optional[List[ServiceResponseModel]] = []
    iata_code: str


class AirportResponseModel(AirportCreateModel):
    id: UUID
    created_at: datetime


class AirportUpdateModel(BaseModel):
    airport_name: Optional[str] = None
    airport_location: Optional[str] = None
    iata_code: Optional[str] = None

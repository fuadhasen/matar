"""module for pydantic validation"""
from pydantic import BaseModel
from sqlmodel import Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class TripCreateModel(BaseModel):
    origin: str = Field(max_length=255)
    destination: str = Field(max_length=255)
    trip_date: str
    price: float
    status: str = Field(default="available", max_length=20)

    class Config:
        orm_mode: True

class TripResponseModel(TripCreateModel):
    id: UUID
    created_at: datetime
    trip_date: datetime

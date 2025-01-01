"""module for pydantic validation"""
from pydantic import BaseModel
from sqlmodel import Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class BookingCreateModel(BaseModel):
    driver_id: str
    trip_id: str
    # user_id: UUID = Field(foreign_key="user.id")
    number_of_passengers: int
    total_price: float
    booking_date: str
    status: str

    class Config:
        orm_mode: True

class BookingResponseModel(BookingCreateModel):
    id: UUID
    created_at: datetime
    driver_id: UUID
    trip_id: UUID
    booking_date: datetime


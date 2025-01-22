"""module for pydantic validation"""

from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class BookingCreateModel(BaseModel):
    service_id: UUID
    tourist_id: UUID
    number_of_passengers: int
    booking_date: datetime

    class Config:
        orm_mode: True


class BookingResponseModel(BookingCreateModel):
    id: UUID
    service_id: UUID
    tourist_id: UUID
    booking_date: datetime
    created_at: datetime

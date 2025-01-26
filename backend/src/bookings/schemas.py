"""module for pydantic validation"""

from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class BookingCreateModel(BaseModel):
    service_id: UUID
    number_of_passengers: int
    booking_date: datetime


class BookingUpdateModel(BaseModel):
    number_of_passengers: Optional[int] = None
    booking_date: Optional[datetime] = None


class BookingResponseModel(BookingCreateModel):
    id: UUID
    service_id: UUID
    booking_date: datetime
    created_at: datetime

"""module for pydantic validation"""

from pydantic import BaseModel
from sqlmodel import Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class ReviewCreateModel(BaseModel):
    service_id: UUID
    rating: int
    comment: Optional[str] = Field(default=None)

    class Config:
        orm_mode: True


class ReviewResponseModel(ReviewCreateModel):
    id: UUID
    service_id: UUID
    tourist_id: UUID
    created_at: datetime

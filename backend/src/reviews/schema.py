"""module for pydantic validation"""
from pydantic import BaseModel
from sqlmodel import Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class ReviewCreateModel(BaseModel):
    driver_id: str
    rating: int
    comment: Optional[str]

    class Config:
        orm_mode: True

class ReviewResponseModel(ReviewCreateModel):
    id: UUID
    created_at: datetime
    driver_id: UUID
    user_id: UUID

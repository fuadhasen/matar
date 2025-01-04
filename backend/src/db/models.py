"""module for Database models
"""
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, ForeignKey
from uuid import UUID, uuid4
import uuid
from uuid import UUID
import sqlalchemy.dialects.postgresql as pg


class RoleEnum(str, Enum):
    tourist = "tourist"
    driver = "driver"


class BaseModel(SQLModel):
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    created_at: datetime = Field(default_factory=datetime.now)


class User(BaseModel, table=True):
    full_name: str = Field(max_length=255)
    email: str = Field(max_length=255, unique=True)
    password: str
    phone_number: Optional[str] = Field(max_length=15)
    role: RoleEnum

    def __repr__(self):
        return f"User: {self}"


class Driver(BaseModel, table=True):
    user_id: UUID = Field(
        sa_column=Column(
            pg.UUID,
            ForeignKey('user.id'),
            nullable=False,
        )
    )
    vehicle_type: str = Field(max_length=50)
    vehicle_registration_number: str = Field(max_length=50, unique=True)
    languages_spoken: Optional[str] = Field(max_length=255)
    experience_years: Optional[int] = Field(default=0)
    verified: bool = Field(default=False)

    def __repr__(self):
        return f"Driver {self}"


class Trip(BaseModel, table=True):
    origin: str = Field(max_length=255)
    destination: str = Field(max_length=255)
    trip_date: datetime
    price: float
    status: str = Field(default="available", max_length=20)


class Booking(BaseModel, table=True):
    driver_id: UUID = Field(foreign_key='driver.id')
    trip_id: UUID = Field(foreign_key="trip.id")
    user_id: UUID = Field(
        sa_column=Column(
            pg.UUID,
            ForeignKey('user.id'),
            nullable=False,
        )
    )
    number_of_passengers: int
    total_price: float
    booking_date: datetime = Field(default_factory=datetime.now)
    status: str = Field(default="pendings", max_length=20)


class Review(BaseModel, table=True):
    driver_id: UUID = Field(foreign_key="driver.id")
    user_id: UUID = Field(
        sa_column=Column(
            pg.UUID,
            ForeignKey('user.id'),
            nullable=False,
        )
    )
    rating: int = Field(ge=1, le=5)
    comment: Optional[str]

    def __repr__(self):
        return f"Review {self}"

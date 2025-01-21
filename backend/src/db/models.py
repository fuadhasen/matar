"""module for Database models
"""

import uuid
import sqlalchemy.dialects.postgresql as pg
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, ForeignKey
from uuid import UUID
from typing import List


class RoleEnum(str, Enum):
    tourist = "tourist"
    driver = "driver"
    admin = "admin"
    staff = "staff"


class BaseModel(SQLModel):
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    created_at: datetime = Field(default_factory=datetime.now)


class User(BaseModel, table=True):
    first_name: str = Field(max_length=255)
    last_name: str = Field(max_length=255)
    email: str = Field(max_length=255, unique=True)
    password: str
    phone_number: Optional[str] = Field(max_length=15)
    role: RoleEnum
    is_active: bool = Field(default=True)

    def __repr__(self):
        return f"User: {self}"


class Airport(BaseModel, table=True):
    airport_name: str = Field(max_length=255)
    airport_location: str = Field(max_length=255)
    iata_code: str = Field(max_length=10)
    services: List["Service"] = Relationship(
        back_populates="airport", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self):
        return f"Airport {self}"


class Driver(BaseModel, table=True):
    user_id: UUID = Field(
        sa_column=Column(
            pg.UUID, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
        )
    )
    languages_spoken: Optional[str] = Field(max_length=255)
    experience_years: Optional[int] = Field(default=0)
    verified: bool = Field(default=False)
    services: List["Service"] = Relationship(
        back_populates="driver", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self):
        return f"Driver {self}"


class Service(BaseModel, table=True):
    vehicle_type: str = Field(max_length=50)
    vehicle_registration_number: str = Field(max_length=50, unique=True)
    vehicle_model: str = Field(max_length=50)
    vehicle_color: str = Field(max_length=50)
    vehicle_capacity: int

    driver_id: UUID = Field(foreign_key="driver.id", ondelete="CASCADE")
    driver: Driver = Relationship(back_populates="services")

    airport_id: UUID = Field(foreign_key="airport.id", ondelete="CASCADE")
    airport: Airport = Relationship(back_populates="services")

    def __repr__(self):
        return f"Vehicle {self}"


class Booking(BaseModel, table=True):
    user_id: UUID = Field(
        sa_column=Column(
            pg.UUID,
            ForeignKey("user.id", ondelete="CASCADE"),
            nullable=False,
        )
    )
    service_id: UUID = Field(
        sa_column=Column(
            pg.UUID,
            ForeignKey("service.id", ondelete="CASCADE"),
            nullable=False,
        )
    )
    number_of_passengers: int
    booking_date: datetime = Field(default_factory=datetime.now)
    status: str = Field(default="pendings", max_length=20)


class Review(BaseModel, table=True):
    service_id: UUID = Field(foreign_key="driver.id", ondelete="CASCADE")
    user_id: UUID = Field(
        sa_column=Column(
            pg.UUID,
            ForeignKey("user.id", ondelete="CASCADE"),
            nullable=False,
        )
    )
    rating: int = Field(ge=1, le=5)
    comment: Optional[str]

    def __repr__(self):
        return f"Review {self}"

"""module for Application Logic"""

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.db.models import User
from fastapi import HTTPException, status
from sqlalchemy import desc
from .schemas import (
    UserCreateModel,
    DriverCreateModel,
    TouristCreateModel,
    DisableModel,
)
from .utils import generate_hash


class UserService:
    """class for User services"""

    async def register_user(
        self,
        user_data: UserCreateModel,
        session: AsyncSession,
    ):
        """register a new user"""
        user_data.password = generate_hash(user_data.password)
        new_user = User(**user_data.model_dump())
        session.add(new_user)
        await session.commit()
        return new_user

    async def update_user(
        self,
        user_id: str,
        user_data: UserCreateModel,
        session: AsyncSession,
    ):
        """update a user"""
        user = await self.get_a_user(user_id, session)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        if user_data.password:
            user_data.password = generate_hash(user_data.password)
        user.update(user_data.model_dump(exclude_none=True))
        session.add(user)
        await session.commit()

    async def register_driver(
        self,
        driver_data: DriverCreateModel,
        session: AsyncSession,
    ):
        """register a new driver"""
        driver_data.password = generate_hash(driver_data.password)
        new_driver = User(**driver_data.model_dump())
        session.add(new_driver)
        await session.commit()
        return new_driver

    async def register_tourist(
        self,
        tourist_data: TouristCreateModel,
        session: AsyncSession,
    ):
        """register a new tourist"""
        tourist_data.password = generate_hash(tourist_data.password)
        tourist_data.verified = True
        new_tourist = User(**tourist_data.model_dump())
        session.add(new_tourist)
        await session.commit()
        return new_tourist

    async def get_users(self, session: AsyncSession):
        """get all users"""
        statement = select(User).order_by(desc(User.created_at))
        res = await session.exec(statement)
        result = res.all()
        return result

    async def get_a_user(
        self,
        user_id: str,
        session: AsyncSession,
    ):
        """get a user by id"""
        statement = select(User).where(User.id == user_id)
        res = await session.exec(statement)
        result = res.first()
        return result if result is not None else None

    async def get_a_user_by_email(
        self,
        email: str,
        session: AsyncSession,
    ):
        """get a user by email"""
        statement = select(User).where(User.email == email)
        res = await session.exec(statement)
        result = res.first()
        return result if result is not None else None

    async def verify_driver(
        self,
        user_id: str,
        session: AsyncSession,
    ):
        """verify a driver"""
        driver = await self.get_a_user(user_id, session)
        if not driver:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found"
            )
        driver.verified = True
        session.add(driver)
        await session.commit()
        return driver

    async def disable_user(
        self,
        user_id: str,
        disable_data: DisableModel,
        session: AsyncSession,
    ):
        """disable a user"""
        user = await self.get_a_user(user_id, session)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        user.is_active = disable_data.is_active
        session.add(user)
        await session.commit()
        return user

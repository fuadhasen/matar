"""module for Application Logic"""

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.db.models import User
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import desc
from pydantic import EmailStr
from .schemas import (
    UserCreateModel,
    UserUpdateModel,
    DriverCreateModel,
    TouristCreateModel,
)
from src.db.models import RoleEnum
from .oauth import create_access_token
from .utils import hash_pass, verify_password


class UserService:
    """class for User services"""

    async def login(
        self,
        form_data: OAuth2PasswordRequestForm,
        session: AsyncSession,
    ):
        """login a user"""
        user = await self.get_a_user_by_email(form_data.username, session)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect email or password",
            )
        hashed_pass = user.password
        if not verify_password(form_data.password, hashed_pass):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect email or password",
            )
        access_token = create_access_token(data={"email": user.email})
        return {"access_token": access_token, "token_type": "bearer"}

    async def register_user(
        self,
        user_data: UserCreateModel,
        session: AsyncSession,
    ):
        """register a new user"""
        user = await self.get_a_user_by_email(user_data.email, session)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
            )
        user_data.password = hash_pass(user_data.password)
        new_user = User(**user_data.model_dump(), role=RoleEnum.staff)
        session.add(new_user)
        await session.commit()
        return new_user

    async def update_user(
        self,
        user_data: UserUpdateModel,
        current_user: dict,
        session: AsyncSession,
    ):
        """update a user"""
        user = await self.get_a_user_by_email(current_user.email, session)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        if user_data.password:
            user_data.password = hash_pass(user_data.password)
        for key, value in user_data.model_dump(exclude_none=True).items():
            setattr(user, key, value)
        session.add(user)
        await session.commit()
        return user

    async def register_driver(
        self,
        driver_data: DriverCreateModel,
        session: AsyncSession,
    ):
        """register a new driver"""
        driver_data.password = hash_pass(driver_data.password)
        new_driver = User(**driver_data.model_dump(), role=RoleEnum.driver)
        session.add(new_driver)
        await session.commit()
        return new_driver

    async def register_tourist(
        self,
        tourist_data: TouristCreateModel,
        session: AsyncSession,
    ):
        """register a new tourist"""
        tourist_data.password = hash_pass(tourist_data.password)
        new_tourist = User(
            **tourist_data.model_dump(), verified=True, role=RoleEnum.tourist
        )
        session.add(new_tourist)
        await session.commit()
        return new_tourist

    async def get_users(self, session: AsyncSession):
        """get all users"""
        statement = select(User).order_by(desc(User.created_at))
        res = await session.exec(statement)
        result = res.all()
        return result

    async def get_drivers(self, session: AsyncSession):
        """get all drivers"""
        statement = (
            select(User)
            .where(User.role == RoleEnum.driver)
            .order_by(desc(User.created_at))
        )
        res = await session.exec(statement)
        result = res.all()
        return result

    async def get_tourists(self, session: AsyncSession):
        """get all tourists"""
        statement = (
            select(User)
            .where(User.role == RoleEnum.tourist)
            .order_by(desc(User.created_at))
        )
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
        driver_email: EmailStr,
        session: AsyncSession,
    ):
        """verify a driver"""
        driver = await self.get_a_user_by_email(driver_email, session)
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
        session: AsyncSession,
    ):
        """disable a user"""
        user = await self.get_a_user(user_id, session)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        user.is_active = False
        session.add(user)
        await session.commit()
        return user

    async def get_me(
        self,
        current_user: dict,
        session: AsyncSession,
    ):
        """get the current user"""
        user = await self.get_a_user_by_email(current_user.email, session)
        return user

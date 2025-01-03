"""module for Application Logic"""
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.db.models import User
from fastapi import HTTPException, status
from sqlalchemy import desc
from .schema import UserCreateModel
from .utils import generate_hash


class UserService:
    """class for user services"""
    async def get_users(self, session: AsyncSession):
        statement = select(User).order_by(desc(User.created_at))
        res = await session.exec(statement)
        result = res.all()
        return result

    async def get_auser_byemail(self, email, session: AsyncSession):
        statement = select(User).where(User.email == email)
        res = await session.exec(statement)
        result = res.first()
        return result if result is not None else None

    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        user_dict = user_data.model_dump()
        new_user = User(**user_dict)

        hashed_pwd = generate_hash(new_user.password)
        new_user.password = hashed_pwd
        session.add(new_user)
        await session.commit()
        return new_user


    async def update_user(self):
        pass

    async def delete_user(self):
        pass

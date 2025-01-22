"""module for Driver Service"""

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy import desc
from src.db.models import User, RoleEnum


class DriverService:
    """class for Driver services"""

    async def get_drivers(self, session: AsyncSession):
        statement = (
            select(User)
            .where(User.role == RoleEnum.driver)
            .order_by(desc(User.created_at))
        )
        res = await session.exec(statement)
        result = res.all()
        return result

    async def get_a_driver(self, driver_id: str, session: AsyncSession):
        statement = select(User).where(
            User.id == driver_id, User.role == RoleEnum.driver
        )
        res = await session.exec(statement)
        result = res.first()
        return result if result is not None else None

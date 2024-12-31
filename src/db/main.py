"""connection with Asyncronus database API
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import Config


DATABASE_URL=Config.DATABASE_URL
engine = AsyncEngine(
    create_engine(
        DATABASE_URL, echo=False
    )
)


async def init_db():
    async with engine.begin() as conn:
        from .models import User
        print('tables are created')
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    Session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with Session() as session:
        return session

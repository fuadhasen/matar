"""Routes module for Authentication"""
from fastapi import APIRouter, Depends
from .schema import UserCreateModel
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .service import UserService


user_service = UserService()

auth_router = APIRouter()

@auth_router.post('/sign-up')
async def create_user(
    user_data: UserCreateModel,
    session:  AsyncSession = Depends(get_session)
):
    
    

    return {'msg': 'very first route of my Application'}



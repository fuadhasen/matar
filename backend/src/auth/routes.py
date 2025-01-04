"""module for Authentication"""
from fastapi import APIRouter, Depends
from .schema import UserCreateModel, UserResponseModel, LoginModel
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .service import UserService
from fastapi import HTTPException, status
from .utils import verify_hash, create_access_token
from datetime import datetime, timedelta
from src.config import Config
from fastapi.responses import JSONResponse
from .dependency import AccessToken, RefreshToken, get_current_user
from typing import List

EXPIRY_TIME=2
access = AccessToken()
refresh = RefreshToken()
user_service = UserService()
auth_router = APIRouter(
    prefix='/api'
)


@auth_router.post('/auth/register', response_model=UserResponseModel)
async def create_user(
    user_data: UserCreateModel,
    session:  AsyncSession = Depends(get_session)
):
    user_email = user_data.email
    user = await user_service.get_auser_byemail(user_email, session)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user is already exist"
        )

    user = await user_service.create_user(user_data, session)
    return user


@auth_router.post('/auth/login')
async def login(
    user_credential: LoginModel,
    session: AsyncSession = Depends(get_session)
):
    email = user_credential.email
    user = await user_service.get_auser_byemail(email, session)
    if user:
       isvalid = verify_hash(user_credential.password, user.password)
       if isvalid:
           access_token = create_access_token(
               user_data={
                   'email': user.email,
                   'id': str(user.id),
                   'role': user.role
               }
           )

           refresh_token = create_access_token(
               user_data={
                   'email': user.email,
                   'id': str(user.id),
                   'role': user.role
               },
               expiry=timedelta(days=EXPIRY_TIME),
               refresh=True
           )

           return JSONResponse(
               content={
                   'message': 'Login Successful',
                   'access_token': access_token,
                   'refresh_token': refresh_token,
                   'user': {
                        'user_id': str(user.id),
                        'user_email': user.email
                    }
                }
            )


@auth_router.get('/users/me', response_model=UserResponseModel)
async def user(
    session: AsyncSession = Depends(get_session),
    token_detail: dict = Depends(access)
):
    user = await get_current_user(session, token_detail)
    return user


# should be access based only for admins.???
@auth_router.get('/admin/users', response_model=List[UserResponseModel])
async def get_users(session: AsyncSession = Depends(get_session)):
    users = await user_service.get_users(session)
    return users


@auth_router.get('/admin/users/{user_id}', response_model=List[UserResponseModel])
async def delete_users(user_id: str, session: AsyncSession = Depends(get_session)):
    users = await user_service.delete_user(user_id, session)
    return users


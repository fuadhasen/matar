"""Routes module for Authentication"""
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

EXPIRY_TIME=2
user_service = UserService()
auth_router = APIRouter()


@auth_router.post('/sign-up', response_model=UserResponseModel)
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


@auth_router.post('/login')
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
                   'uuid': str(user.id),
                   'role': user.role
               }
           )

           refresh_token = create_access_token(
               user_data={
                   'email': user.email,
                   'uuid': str(user.id),
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



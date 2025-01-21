"""module for Authentication"""

from fastapi import APIRouter, Depends
from .schemas import UserCreateModel, UserResponseModel, LoginModel, DisableModel
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .service import UserService
from fastapi import HTTPException, status
from .utils import verify_hash, create_access_token
from datetime import datetime, timedelta
from src.config import Config
from fastapi.responses import JSONResponse
from .dependency import AccessToken, RefreshToken, get_current_user, RoleChecker
from src.drivers.routes import driver_service
from src.drivers.schemas import DriverCreateModel
from typing import List


EXPIRY_TIME = 2
access = AccessToken()
refresh = RefreshToken()
refresh = RefreshToken()
user_service = UserService()

auth_router = APIRouter(prefix="/api")


@auth_router.post("/auth/register", response_model=UserResponseModel)
async def create_user(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):
    user_email = user_data.email
    user = await user_service.get_auser_byemail(user_email, session)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="user is already exist"
        )

    user = await user_service.create_user(user_data, session)
    return user


@auth_router.post("/driver/apply", response_model=UserResponseModel)
@auth_router.post("/auth/login")
async def login(
    user_credential: LoginModel, session: AsyncSession = Depends(get_session)
):
    email = user_credential.email
    user = await user_service.get_auser_byemail(email, session)
    if user:
        isvalid = verify_hash(user_credential.password, user.password)
        if isvalid:
            access_token = create_access_token(
                user_data={"email": user.email, "id": str(user.id), "role": user.role}
            )

            refresh_token = create_access_token(
                user_data={"email": user.email, "id": str(user.id), "role": user.role},
                expiry=timedelta(days=EXPIRY_TIME),
                refresh=True,
            )

            return JSONResponse(
                content={
                    "message": "Login Successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {"id": str(user.id), "email": user.email},
                }
            )


@auth_router.get("/refresh_token")
async def refresh(token_detail: dict = Depends(refresh)):
    expiry = token_detail["exp"]
    if datetime.fromtimestamp(expiry) > datetime.now():
        user_data = token_detail["user"]
        access_token = create_access_token(user_data)
        return access_token
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid or expired access token",
    )


@auth_router.get("/users/me", response_model=UserResponseModel)
async def user(
    user: dict = Depends(get_current_user), token_detail: dict = Depends(access)
):
    return user


@auth_router.get("/admin/users", response_model=List[UserResponseModel])
async def get_users(
    session: AsyncSession = Depends(get_session),
    token_detail: dict = Depends(access),
    role: bool = Depends(RoleChecker(["admin", "staff"])),
):
    users = await user_service.get_users(session)
    return users


@auth_router.patch("/admin/users/{user_id}")
async def disable_user(
    user_id: str,
    user_data: DisableModel,
    session: AsyncSession = Depends(get_session),
    token_detail: dict = Depends(access),
    role: bool = Depends(RoleChecker(["admin", "staff"])),
):
    users = await user_service.disable_user(user_id, user_data, session)
    return JSONResponse(content={"message": f"user with this {user_id} id is disabled"})

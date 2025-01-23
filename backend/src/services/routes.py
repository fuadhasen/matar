"""module for Drivers Resource"""

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from .services import DriverService
from src.db.main import get_session
from typing import List
from src.users.dependency import AccessToken
from src.users.services import UserService
from src.users.dependency import RoleChecker


user_service = UserService()
driver_router = APIRouter(
    prefix="/api",
    tags=["Drivers"],
)

driver_service = DriverService()
access = AccessToken()





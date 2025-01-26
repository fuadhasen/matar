"""module for Drivers Resource"""

from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.users.services import UserService
from src.users.oauth import verify_is_driver
from .services import DriverService
from .schemas import ServiceCreateModel, ServiceResponseModel
from uuid import UUID

user_service = UserService()
router = APIRouter(
    prefix="/api/drivers",
    tags=["Driver Services"],
)

driver_service = DriverService()


@router.post(
    "/services",
    status_code=status.HTTP_201_CREATED,
    response_model=ServiceResponseModel,
    summary="Create a service",
)
async def create_a_service(
    service: ServiceCreateModel,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(verify_is_driver),
):
    """create a service"""
    user_id = current_user.id
    service_data = {**service.model_dump(), "user_id": user_id}
    return await driver_service.create_a_service(session, service_data)


@router.put(
    "/services/{service_id}",
    response_model=ServiceResponseModel,
    summary="Update a service",
)
async def update_a_service(
    service_id: UUID,
    service: ServiceCreateModel,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(verify_is_driver),
):
    """update a service"""
    service_data = {**service.model_dump(exclude_none=True)}
    return await driver_service.update_a_service(session, service_id, service_data)


@router.delete(
    "/services/{service_id}",
    summary="Delete a service",
)
async def delete_a_service(
    service_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(verify_is_driver),
):
    """delete a service"""
    return await driver_service.delete_a_service(session, service_id)

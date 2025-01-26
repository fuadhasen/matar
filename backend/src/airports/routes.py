"""module for Drivers Resource"""

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID
from typing import List
from src.db.main import get_session
from .services import AirportService
from .schemas import AirportCreateModel, AirportUpdateModel, AirportResponseModel
from src.users.oauth import verify_is_staff

router = APIRouter(prefix="/airports", tags=["Airports"])
airport_service = AirportService()


@router.get(
    "/",
    response_model=List[AirportResponseModel],
    status_code=status.HTTP_200_OK,
    summary="Get all airports",
)
async def get_airports(
    session: AsyncSession = Depends(get_session),
):
    """get all airports"""
    result = await airport_service.get_airports(session)
    return result


@router.get(
    "/{airport_id}",
    response_model=AirportResponseModel,
    status_code=status.HTTP_200_OK,
    summary="Get an airport",
)
async def get_an_airport(
    airport_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    """get an airport"""
    result = await airport_service.get_an_airport(airport_id, session)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Airport not found",
        )
    return result


@router.post(
    "/",
    response_model=AirportResponseModel,
    status_code=status.HTTP_201_CREATED,
    summary="Create an airport",
)
async def create_airport(
    airport_data: AirportCreateModel,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(verify_is_staff),
):
    """create an airport"""
    result = await airport_service.create_airport(airport_data, session)
    return result


@router.put(
    "/{airport_id}",
    response_model=AirportResponseModel,
    status_code=status.HTTP_200_OK,
    summary="Update an airport",
)
async def update_airport(
    airport_id: UUID,
    airport_data: AirportUpdateModel,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(verify_is_staff),
):
    """update an airport"""
    result = await airport_service.update_airport(airport_id, airport_data, session)
    return result


@router.delete(
    "/{airport_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an airport",
)
async def delete_airport(
    airport_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(verify_is_staff),
):
    """delete an airport"""
    await airport_service.delete_airport(airport_id, session)
    return JSONResponse(content={"message": "airport deleted successfully"})


@router.get(
    "/search/{search_term}",
    response_model=List[AirportResponseModel],
    status_code=status.HTTP_200_OK,
    summary="Search airports",
)
async def search_airports(
    search_term: str, session: AsyncSession = Depends(get_session)
):
    """search airports"""
    result = await airport_service.search_airports(search_term, session)
    return result

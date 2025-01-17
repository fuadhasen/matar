"""module for Reviews Resource"""

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import ReviewService
from .schemas import ReviewCreateModel, ReviewResponseModel
from src.db.main import get_session
from uuid import UUID
from typing import List
from src.auth.dependency import AccessToken, RoleChecker


access = AccessToken()
review_router = APIRouter(prefix="/api")
review_service = ReviewService()


@review_router.post(
    "/reviews",
    response_model=ReviewResponseModel,
    tags=["Reviews endpoints"],
)
async def create_review(
    review_data: ReviewCreateModel,
    session: AsyncSession = Depends(get_session),
    token_detail: dict = Depends(access),
    role: bool = Depends(RoleChecker(["tourist"])),
):
    user_id = token_detail["user"]["id"]
    review = await review_service.create_review(user_id, review_data, session)
    return review


@review_router.get(
    "/drivers/{driver_id}/reviews",
    response_model=List[ReviewResponseModel],
    tags=["Reviews endpoints"],
)
async def get_a_review(
    driver_id: str,
    session: AsyncSession = Depends(get_session),
    token_detail: dict = Depends(access),
    role: bool = Depends(RoleChecker(["driver"])),
):
    review = await review_service.get_a_review_by_driverid(driver_id, session)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="not review for this driver"
        )
    return review

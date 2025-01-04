"""module for Reviews Resource"""
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import ReviewService
from .schema import ReviewCreateModel, ReviewResponseModel
from src.db.main import get_session
from uuid import UUID
from typing import List
from src.auth.dependency import AccessToken

access = AccessToken()

review_router = APIRouter(
    prefix='/api'
)
review_service = ReviewService()


# dont forget role based access
@review_router.post('/reviews', response_model=ReviewResponseModel)
async def create_review(
    review_data: ReviewCreateModel,
    session: AsyncSession = Depends(get_session),
    token_detail: dict = Depends(access)
):
    user_id = token_detail['user']['user_id']
    review = await review_service.create_review(user_id, review_data, session)
    return review


@review_router.get('/drivers/{driver_id}/reviews', response_model=ReviewResponseModel)
async def get_a_review(
    driver_id: str,
    session: AsyncSession = Depends(get_session),
    token_detail: dict = Depends(access)
):
    review = await review_service.get_a_review_by_driverid(driver_id, session)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="driver Not found"
        )
    return review

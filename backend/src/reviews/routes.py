"""module for Reviews Resource"""
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import ReviewService
from .schema import ReviewCreateModel, ReviewResponseModel
from src.db.main import get_session
from uuid import UUID
from typing import List


review_router = APIRouter(
    prefix='/api'
)
review_service = ReviewService()


@review_router.get('/reviews', response_model=List[ReviewResponseModel])
async def get_reviews(session: AsyncSession = Depends(get_session)):
    reviews = await review_service.get_reviews(session)
    return reviews


@review_router.get('/review/{review_id}', response_model=ReviewResponseModel)
async def get_a_review(review_id: str, session: AsyncSession = Depends(get_session)):
    review = await review_service.get_a_review(review_id, session)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="driver Not found"
        )
    return review


# create reviews
@review_router.post('/reviews', response_model=ReviewResponseModel)
async def create_review(
    review_data: ReviewCreateModel,
    session: AsyncSession = Depends(get_session)
):
    review = await review_service.create_review(review_data, session)
    return review


@review_router.get('/drivers/{driver_id}/reviews', response_model=ReviewResponseModel)
async def get_a_review(review_id: str, session: AsyncSession = Depends(get_session)):
    review = await review_service.get_a_review(review_id, session)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="driver Not found"
        )
    return review

# @review_router.patch('/review/{review_id}')
# async def update_review(
#     review_id: str,
#     review_data: ReviewCreateModel,
#     session: AsyncSession = Depends(get_session)
# ):
#     review = await review_service.update_review(review_id, review_data, session)
#     return review


# @review_router.delete('/review/{review_id}')
# async def delete_review(review_id: str, session: AsyncSession = Depends(get_session)):
#     review = await review_service.delete_review(review_id, session)
#     return review

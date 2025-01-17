"""module for Reviews Service"""
from fastapi import status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy import desc
from src.db.models import Review
from fastapi.exceptions import HTTPException
from .schemas import ReviewCreateModel
from uuid import UUID
from src.drivers.routes import driver_service


class ReviewService:
    """class for Review services"""
    async def get_reviews(self, session: AsyncSession):
        statement = select(Review).order_by(desc(Review.created_at))
        res = await session.exec(statement)
        result = res.all()
        return result

    async def get_a_review(self, review_id: str, session: AsyncSession):
        statement = select(Review).where(Review.id == review_id)
        res = await session.exec(statement)
        result = res.first()
        return result if result is not None else None

    async def get_a_review_by_driverid(self, driver_id: str, session: AsyncSession):
        statement = select(Review).where(Review.driver_id == driver_id)
        res = await session.exec(statement)
        result = res.all()
        return result if result is not None else None

    async def create_review(self, user_id, review_data: ReviewCreateModel, session: AsyncSession):
        driver_id = review_data.driver_id
        driver = await driver_service.get_a_driver(driver_id, session)
        if not driver:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="driver not found"
                            )

        statement = select(Review).where(Review.user_id == user_id and Review.driver_id == driver.id)
        res = await session.exec(statement)
        review = res.first()
        if review:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Cant Review a driver more than one'
            )
        new_data = review_data.model_dump()

        new_review = Review(**new_data)
        new_review.user_id = user_id
        new_review.driver_id = UUID(new_data['driver_id'])
        session.add(new_review)
        await session.commit()
        return new_review

    async def update_review(self, review_id: str, review_data: ReviewCreateModel, session: AsyncSession):
        review = await self.get_a_review(review_id, session)
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review Not found"
            )

        new_data = review_data.model_dump()
        review.driver_id = UUID(new_data['driver_id'])
        for k, v in new_data.items():
            if (k != 'driver_id'):
                setattr(review, k, v)
        await session.commit()
        return review

    async def delete_review(self, review_id: str, session: AsyncSession):
        review = await self.get_a_review(review_id, session)
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found"
            )

        await session.delete(review)
        await session.commit()
        return {}

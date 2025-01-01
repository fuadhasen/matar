"""Entry Point of the Application"""
from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.auth.routes import auth_router
from src.drivers.routes import driver_router
from src.bookings.routes import booking_router
from src.trips.routes import trip_router
from src.reviews.routes import review_router


@asynccontextmanager
async def life_span(app: FastAPI):
    print("server is running")
    await init_db()
    yield
    print("server is finished")

version = 1

app = FastAPI(
    title='Api && Integration',
    description='FastAPI backend Application',
    version=version
    # lifespan=life_span
)

app.include_router(auth_router)
app.include_router(driver_router)
app.include_router(trip_router)
app.include_router(booking_router)
app.include_router(review_router)

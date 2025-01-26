"""Entry Point of the Application"""

from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.users.routes import router as user_router
from src.airports.routes import router as airport_router
from src.services.routes import router as service_router
from src.bookings.routes import router as booking_router
from src.config import Config


@asynccontextmanager
async def life_span(app: FastAPI):
    print("server is running")
    await init_db()
    yield
    print("server is finished")


app = FastAPI(
    title=Config.APP_NAME,
    description=Config.DESC,
    version=Config.API_VERSION,
    lifespan=life_span,
)


app.include_router(user_router)
app.include_router(airport_router)
app.include_router(service_router)
app.include_router(booking_router)

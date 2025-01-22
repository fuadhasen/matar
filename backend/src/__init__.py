"""Entry Point of the Application"""

from fastapi import FastAPI, APIRouter, Depends
from contextlib import asynccontextmanager
from src.db.main import init_db, get_session
from src.users.schemas import UserResponseModel
from src.users.services import UserService
from src.users.routes import auth_router
from src.airports.routes import router as airport_router
from src.services.routes import driver_router
from src.bookings.routes import booking_router
from src.reviews.routes import review_router
from src.config import Config


# def admin_register(app: FastAPI):
#     router = APIRouter()

#     @router.post(
#         "/api/admin/register",
#         response_model=UserResponseModel,
#         tags=["Admin"],
#     )
#     async def temp_route(user_data: AdminCreateModel, session=Depends(get_session)):
#         """Temporary route to register an admin"""
#         app.router.routes.remove(router.routes[0])
#         user_service = UserService()
#         user = await user_service.create_user(user_data, session)
#         return user

#     app.include_router(router)


@asynccontextmanager
async def life_span(app: FastAPI):
    print("server is running")
    await init_db()
    # admin_register(app)
    yield
    print("server is finished")


app = FastAPI(
    title=Config.APP_NAME,
    description=Config.DESC,
    version=Config.API_VERSION,
    lifespan=life_span,
)


# app.include_router(auth_router)
app.include_router(driver_router)
app.include_router(airport_router)
# app.include_router(trip_router)
# app.include_router(booking_router)
# app.include_router(review_router)

"""Entry Point of the Application"""
from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.auth.routes import auth_router

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

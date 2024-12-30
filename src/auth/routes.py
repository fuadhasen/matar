"""Routes module for Authentication"""
from fastapi import APIRouter


auth_router = APIRouter()

@auth_router.get('/')
async def index():
    return {'msg': 'very first route of my Application'}



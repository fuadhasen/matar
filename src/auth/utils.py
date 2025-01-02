"""utility functions that support the Application"""
from passlib.context import CryptContext
import jwt
from datetime import timedelta, datetime
from src.config import Config


EXPIRY_TIME=3600
password_context = CryptContext(
    schemes=['bcrypt']
)


def generate_hash(password: str):
    """to generate the hashed password"""
    hash = password_context.hash(password)
    return hash

def verify_hash(password: str, hashed_pwd: str):
    """verify the hashed password"""
    return password_context.verify(password, hashed_pwd)

def create_access_token(user_data: dict, expiry: timedelta=None, refresh: bool=False):
    """access token creating method"""
    print(f'alen: {expiry}')
    payload={}
    payload['user'] = user_data
    payload['exp'] = datetime.now() + (expiry if expiry is not None else timedelta(seconds=EXPIRY_TIME))
    payload['refresh'] = refresh

    token = jwt.encode(
        payload=payload,
        key=Config.SECRET_KEY,
        algorithm=Config.ALGORITHM
    )
    return token


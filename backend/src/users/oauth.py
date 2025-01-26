from datetime import timedelta, datetime, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from pydantic import EmailStr
from src.db.main import get_session
from src.db.models import User, RoleEnum
from src.users.schemas import DataToken
from src.config import Config


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

SECRET_KEY = Config.SECRET_KEY
ALGORITHM = Config.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = Config.EXPIRY_TIME


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"expire": expire.strftime("%Y-%m-%d %H:%M:%S")})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return encoded_jwt


def verify_token_access(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        email: EmailStr = payload.get("email")

        if id is None:
            raise credentials_exception
        token_data = DataToken(email=email)
    except JWTError as e:
        print(e)
        raise credentials_exception

    return token_data


async def get_current_user(
    token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not Validate Credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_token_access(token, credentials_exception)
    statement = select(User).where(User.email == token.email)
    res = await session.exec(statement)
    user = res.first()
    if user is None:
        raise credentials_exception
    return user


async def verify_is_staff(current_user: User = Depends(get_current_user)):
    print(current_user.role == RoleEnum.staff or current_user.role == RoleEnum.admin)
    if not (current_user.role == RoleEnum.staff or current_user.role == RoleEnum.admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Permission Denied"
        )
    return current_user


async def verify_is_driver(current_user: User = Depends(get_current_user)):
    if not current_user.verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account not verified, please contact admin",
        )
    if not current_user.role == RoleEnum.driver and current_user.verified is True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Permission Denied"
        )
    return current_user


async def verify_is_tourist(current_user: User = Depends(get_current_user)):
    if not current_user.role == RoleEnum.tourist:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Permission Denied"
        )
    return current_user

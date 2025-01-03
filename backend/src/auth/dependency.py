"""Token verification module"""
from fastapi.security import HTTPBearer
from fastapi import Request
from .utils import decode_token
from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import UserService

user_service = UserService()


class TokenBearer(HTTPBearer):
    """class for token validation"""
    def __init__(self, auto_error=True):
        super().__init__(auto_error=True)

    async def __call__(self, request: Request):
        creds = await super().__call__(request)
        token = creds.credentials

        token_data = decode_token(token)
        if not self.validate_token(token):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="token invalid or expired"
                            )

        # token revoking implemented here.

        self.verify_token_data(token_data)
        return token_data

    def validate_token(self, token):
        token_data = decode_token(token)
        return True if token_data is not None else False
    def verify_token_data(self, token_data):
        raise NotImplementedError('Please implement this in child classes')


class AccesToken(TokenBearer):
    """access_token validation"""
    def verify_token_data(self, token_data):
        if (token_data and token_data['refresh']):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="please provide access token"
            )


class RefreshToken(TokenBearer):
    """refresh_token validation"""
    def verify_token_data(self, token_data):
        if (token_data and not token_data['refresh']):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="please provide refresh token"
            )


async def get_current_user(
    session: AsyncSession,
    token_detail: dict
):
    email = token_detail['user']['email']
    user = await user_service.get_auser_byemail(email, session)
    return user
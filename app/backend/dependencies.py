from typing import Annotated

from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED

from app.backend.const import Roles, ErrorTexts
from app.services.auth import AuthService


class CustomHTTPBearer(HTTPBearer):
    """Кастомные Bearer для прописывания своих ошибок"""

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        try:
            credentials = await super().__call__(request)
            return credentials
        except HTTPException:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail=ErrorTexts.UNAUTHORIZED_USER
            )


oauth2_scheme = CustomHTTPBearer()


def check_jwt_token(token: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)]) -> dict:
    """Проверяет есть ли токен у пользователя"""

    return AuthService.verify_jwt_token(token.credentials)


def check_permission(required_role: Roles):
    """Проверяет роль пользователя"""

    def role_checker(token: Annotated[dict, Depends(check_jwt_token)]) -> dict:
        if token.get("role") != required_role:
            raise HTTPException(status_code=403, detail=ErrorTexts.NO_PERMISSION)
        return token

    return role_checker

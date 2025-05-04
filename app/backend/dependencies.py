from typing import Annotated

from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED

from app.backend.const import Roles
from app.services.auth import AuthService


class CustomHTTPBearer(HTTPBearer):
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        try:
            credentials = await super().__call__(request)
            return credentials
        except HTTPException:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Неавторизованный пользователь"
            )


oauth2_scheme = CustomHTTPBearer()


def check_jwt_token(token: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)]) -> dict:
    return AuthService.verify_jwt_token(token.credentials)


def check_permission(required_role: Roles):
    def role_checker(token: Annotated[dict, Depends(check_jwt_token)]) -> dict:
        if token.get("role") != required_role:
            raise HTTPException(status_code=403, detail="Пользователь не имеет прав доступа для этой операции"
)
        return token
    return role_checker

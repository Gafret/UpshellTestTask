from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from app.backend.const import SuccessTexts
from app.backend.openapi.responses import AuthRouteResponses
from app.backend.session import SessionDependency
from app.schemas.auth import SignupRequest, SuccessResponse, LoginRequest, TokenPair, RefreshToken, AccessToken
from app.services.auth import AuthService

router = APIRouter(tags=["Пользователи"])


@router.post("/register",
             status_code=HTTP_201_CREATED,
             name="Регистрация нового пользователя",
             description="Регистрирует нового пользователя",
             responses=AuthRouteResponses.REGISTER)
async def register_user(user_data: SignupRequest, session: SessionDependency) -> SuccessResponse:
    created_user = AuthService(session).signup_user(user_data)
    return SuccessResponse(message=SuccessTexts.USER_REGISTERED, user_uuid=created_user.id)


@router.post("/login",
             status_code=HTTP_200_OK,
             name="Логин пользователя",
             description="Аутентифицирует аккаунт пользователя",
             responses=AuthRouteResponses.LOGIN)
async def authenticate_user(login_data: LoginRequest, session: SessionDependency) -> TokenPair:
    tokens = AuthService(session).authenticate_user(login_data)
    return tokens


@router.post("/refresh",
             status_code=HTTP_200_OK,
             name="Обновление access-токена",
             description="Обновляет access-токен на основе действующего refresh-токена.",
             responses=AuthRouteResponses.REFRESH)
async def refresh_access_token(token: RefreshToken) -> AccessToken:
    new_access_token = AuthService.refresh_user_access_token(token)

    return new_access_token

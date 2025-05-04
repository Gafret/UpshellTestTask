from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from app.backend.openapi import AuthRouteResponses
from app.backend.session import SessionDependency
from app.schemas.auth import SignupRequest, SuccessResponse, LoginRequest, TokenPair, RefreshToken, AccessToken
from app.services.auth import AuthService

router = APIRouter(tags=["Пользователи"])


@router.post("/register",
             status_code=HTTP_201_CREATED,
             name="Регистрация нового пользователя",
             description="Регистрирует нового пользователя",
             responses=AuthRouteResponses.register_responses)
async def register_user(user_data: SignupRequest, session: SessionDependency) -> SuccessResponse:
    created_user = AuthService(session).signup_user(user_data)
    return SuccessResponse(message="Регистрация прошла успешно", user_uuid=created_user.id)


@router.post("/login",
             status_code=HTTP_200_OK,
             name="Логин пользователя",
             description="Аутентифицирует аккаунт пользователя",
             responses=AuthRouteResponses.login_responses)
async def authenticate_user(login_data: LoginRequest, session: SessionDependency) -> TokenPair:
    tokens = AuthService(session).authenticate_user(login_data)
    return tokens


@router.post("/refresh",
             status_code=HTTP_200_OK,
             name="Обновление access-токена",
             description="Обновляет access-токен на основе действующего refresh-токена.",
             responses=AuthRouteResponses.refresh_responses)
async def refresh_access_token(token: RefreshToken) -> AccessToken:
    user_data = AuthService.verify_jwt_token(token.refresh_token)
    if user_data.get("type") != "refresh_token":
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Неверный тип токена")
    access_token = AuthService.create_jwt_token(user_data)

    return AccessToken(access_token=access_token)

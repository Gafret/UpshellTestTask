from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, \
    HTTP_401_UNAUTHORIZED

from app.backend.session import SessionDependency
from app.schemas.auth import SignupRequest, SuccessResponse, LoginRequest, TokenPair, RefreshToken, AccessToken
from app.services.auth import AuthService

router = APIRouter(tags=["auth"])


@router.post("/register",
             status_code=HTTP_201_CREATED,
             description="Регистрирует пользователя в магазине",
             responses={
                 HTTP_201_CREATED: {"description": "Пользователь успешно зарегистрирован"},
                 HTTP_400_BAD_REQUEST: {"description": "Отправленная информация не прошла валидацию"},
                 HTTP_409_CONFLICT: {"description": "Пользователь с таким email уже существует"}
             })
async def register_user(user_data: SignupRequest, session: SessionDependency) -> SuccessResponse:
    created_user = AuthService(session).signup_user(user_data)
    return SuccessResponse(message="Регистрация прошла успешно", user_uuid=created_user.id)


@router.post("/login",
             status_code=HTTP_200_OK,
             description="Аутентифицирует аккаунт пользователя",
             responses={
                 HTTP_200_OK: {"description": "Аутентификация прошла успешно"},
                 HTTP_400_BAD_REQUEST: {"description": "Отправленная информация не прошла валидацию"},
             })
async def authenticate_user(login_data: LoginRequest, session: SessionDependency) -> TokenPair:
    tokens = AuthService(session).authenticate_user(login_data)
    return tokens


@router.post("/refresh",
             status_code=HTTP_200_OK,
             description="Обновляет access токен пользователя",
             responses={
                 HTTP_200_OK: {"description": "Access токен обновлен"},
                 HTTP_400_BAD_REQUEST: {"description": "Что-то не так с отправленным токеном"},
                 HTTP_401_UNAUTHORIZED: {"description": "Нет информации для проведения авторизации"},
             })
async def refresh_access_token(token: RefreshToken) -> AccessToken:
    user_data = AuthService.verify_jwt_token(token.refresh_token)
    if user_data.get("type") != "refresh_token":
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Неверный тип токена")
    access_token = AuthService.create_jwt_token(user_data)

    return AccessToken(access_token=access_token)

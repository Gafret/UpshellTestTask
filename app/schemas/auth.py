import uuid

from pydantic import BaseModel, Field, EmailStr

from app.backend.openapi.schema_examples import AuthSchemas
from app.utils.validators import PasswordField, LoginPasswordField, TokenField


class SignupRequest(BaseModel):
    """Модель запроса на регистрацию"""

    email: EmailStr = Field(description="Почта пользователя")
    password: PasswordField = Field(description="Пароль пользователя")

    class Config:
        extra = "forbid"
        json_schema_extra = AuthSchemas.SIGNUP_REQUEST


class SuccessResponse(BaseModel):
    """Модель ответа успешной регистрации"""

    message: str = Field(description="Сообщение об удачной регистрации", max_length=100)
    user_uuid: uuid.UUID = Field(serialization_alias="user_id", description="ID созданного аккаунта")

    class Config:
        json_schema_extra = AuthSchemas.SUCCESS_RESPONSE


class RefreshToken(BaseModel):
    """Модель refresh токена"""

    refresh_token: TokenField = Field(description="Refresh токен")

    class Config:
        json_schema_extra = AuthSchemas.REFRESH_TOKEN


class AccessToken(BaseModel):
    """Модель access токена"""

    access_token: TokenField = Field(description="Access токен")

    class Config:
        json_schema_extra = AuthSchemas.ACCESS_TOKEN


class TokenPair(BaseModel):
    """Модель пары refresh/access токенов, получаемая после логина"""

    access_token: TokenField = Field(description="Access токен")
    refresh_token: TokenField = Field(description="Refresh токен")

    class Config:
        json_schema_extra = AuthSchemas.TOKEN_PAIR


class LoginRequest(SignupRequest):
    """Модель запроса на логин"""

    password: LoginPasswordField = Field(description="Пароль пользователя")

    class Config:
        extra = "forbid"
        json_schema_extra = AuthSchemas.LOGIN_REQUEST

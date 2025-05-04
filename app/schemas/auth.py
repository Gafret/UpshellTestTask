import uuid
from typing import Annotated

from pydantic import BaseModel, Field, EmailStr

from app.utils.validators import PasswordField, LoginPasswordField

TokenField = Annotated[str, Field(min_length=32, max_length=256)]


class SignupRequest(BaseModel):
    """Модель запроса на регистрацию"""

    email: EmailStr = Field(description="Почта пользователя")
    password: PasswordField = Field(description="Пароль пользователя")

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "email": "example@domain.com",
                    "password": "Password123"
                }
            ]
        }


class SuccessResponse(BaseModel):
    """Модель ответа успешной регистрации"""

    message: str = Field(description="Сообщение об удачной регистрации", max_length=100)
    user_uuid: uuid.UUID = Field(serialization_alias="user_id", description="ID созданного аккаунта")

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "message": "Регистрация прошла успешно",
                    "userId": "123e4567-e89b-12d3-a456-426614174000"
                }
            ]
        }


class RefreshToken(BaseModel):
    """Модель refresh токена"""

    refresh_token: TokenField = Field(description="Refresh токен")

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                }
            ]
        }


class AccessToken(BaseModel):
    """Модель access токена"""

    access_token: TokenField = Field(description="Access токен")

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                }
            ]
        }


class TokenPair(BaseModel):
    """Модель пары refresh/access токенов, получаемая после логина"""

    access_token: TokenField = Field(description="Access токен")
    refresh_token: TokenField = Field(description="Refresh токен")

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "access_token": "eyJhbGciOiJIUzI1...",
                    "refresh_token": "eyJhbGciOiJIUzI1..."
                }
            ]
        }


class LoginRequest(SignupRequest):
    """Модель запроса на логин"""

    password: LoginPasswordField = Field(description="Пароль пользователя")

    class Config:
        extra = "forbid"
        json_schema_extra = {
            "examples": [
                {
                    "email": "user@example.com",
                    "password": "pa$$w0rd123"
                }
            ]
        }

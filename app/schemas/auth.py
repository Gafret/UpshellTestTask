import uuid
from typing import Annotated

from pydantic import BaseModel, Field, EmailStr

from app.utils.validators import PasswordField


TokenField = Annotated[str, Field(min_length=32, max_length=256)]


class SignupRequest(BaseModel):
    """Модель запроса на регистрацию"""

    email: EmailStr = Field(description="Почта пользователя")
    password: PasswordField = Field(description="Пароль пользователя")


class SuccessResponse(BaseModel):
    """Модель ответа успешной регистрации"""

    message: str = Field(description="Сообщение об удачной регистрации", max_length=100)
    user_uuid: uuid.UUID = Field(serialization_alias="user_id", description="ID созданного аккаунта")


class RefreshToken(BaseModel):
    """Модель refresh токена"""

    refresh_token: TokenField = Field(description="Refresh токен")


class AccessToken(BaseModel):
    """Модель access токена"""

    access_token: TokenField = Field(description="Access токен")


class TokenPair(BaseModel):
    """Модель пары refresh/access токенов, получаемая после логина"""

    access_token: TokenField = Field(description="Access токен")
    refresh_token: TokenField = Field(description="Refresh токен")


class LoginRequest(SignupRequest):
    """Модель запроса на логин"""

    class Config:
        extra = "forbid"

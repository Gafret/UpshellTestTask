import datetime as dt
from datetime import timedelta, datetime

import jwt
from fastapi import HTTPException
from passlib.context import CryptContext
from sqlmodel import select
from starlette.status import HTTP_409_CONFLICT, HTTP_400_BAD_REQUEST

from app.backend.config import config
from app.backend.const import Roles, ErrorTexts
from app.models.auth import User
from app.schemas.auth import SignupRequest, LoginRequest, TokenPair, RefreshToken, AccessToken
from app.services.base import BaseService, BaseDataManager

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class HashingMixin:
    """Миксин, дающий необходимый минимум для работы с хешированием"""

    @staticmethod
    def bcrypt(value: str) -> str:
        return pwd_context.hash(value)

    @staticmethod
    def verify(plain_value: str, hashed_value: str) -> bool:
        return pwd_context.verify(plain_value, hashed_value)


class JWTTokenMixin:
    """Миксин, дающий необходимый минимум для работы с JWT"""

    @staticmethod
    def create_jwt_token(data: dict, expires_delta=timedelta(minutes=config.access_token_ttl_minutes)):
        to_encode = data.copy()
        expire = datetime.now(dt.UTC) + expires_delta  # Устанавливаем время жизни токена
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, config.secret_key, algorithm=config.hash_algo)

    @staticmethod
    def verify_jwt_token(token: str):
        try:
            payload = jwt.decode(token, config.secret_key, algorithms=[config.hash_algo])
            return payload
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=ErrorTexts.INVALID_OR_EXPIRED_TOKEN)


class AuthService(BaseService, HashingMixin, JWTTokenMixin):
    """Сервис, отвечающий за все, связанное с аутентификацией"""

    def authenticate_user(self, login_data: LoginRequest):
        """Аутентифицирует пользователя по паролю и почте, выдавая пару токенов (access, refresh)"""

        repo = AuthDataManager(self.session)
        user = repo.get_user_by_email(login_data.email)

        if (user is None) or (not AuthService.verify(login_data.password, user.hashed_password)):
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=ErrorTexts.INVALID_PASS_OR_EMAIL)

        role = user.role_id
        access_token = AuthService.create_jwt_token({"iss": user.email, "type": "access_token", "role": role})
        refresh_token = AuthService.create_jwt_token(
            {"iss": user.email, "type": "refresh_token"},
            expires_delta=timedelta(minutes=config.refresh_token_ttl_minutes),
        )

        return TokenPair(access_token=access_token, refresh_token=refresh_token)

    def signup_user(self, signup_data: SignupRequest) -> User:
        """Регистрирует пользователя"""

        repo = AuthDataManager(self.session)
        if repo.get_user_by_email(signup_data.email):
            raise HTTPException(status_code=HTTP_409_CONFLICT, detail=ErrorTexts.USER_ALREADY_EXISTS)

        # Сделано для формирования админа на тестах, не хочется в публичном API отправлять
        # значение роли, дающее пользователям возможности админа
        if signup_data.email == "admin@domain.com" and signup_data.password == "Admin1234":
            user = User(
                email=signup_data.email,
                hashed_password=self.bcrypt(signup_data.password),
                role_id=Roles.ADMIN
            )
        else:
            user = User(
                email=signup_data.email,
                hashed_password=self.bcrypt(signup_data.password)
            )

        db_user = repo.add_user(user)

        return db_user

    @staticmethod
    def refresh_user_access_token(refresh_token: RefreshToken) -> AccessToken:
        user_data = AuthService.verify_jwt_token(refresh_token.refresh_token)
        if user_data.get("type") != "refresh_token":
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=ErrorTexts.INVALID_TOKEN_TYPE)
        access_token = AuthService.create_jwt_token(user_data)

        return AccessToken(access_token=access_token)


class AuthDataManager(BaseDataManager):
    """Сервис, представляющий собой репозиторий для модели пользователя"""

    def add_user(self, user: User) -> User:
        self.add_one(user)
        self.session.commit()
        self.session.refresh(user)

        return user

    def get_user_by_email(self, email: str) -> User | None:
        query = select(User).where(User.email == email)
        model = self.get_one(query)

        if model is not None:
            return User(**model.model_dump())

        return None

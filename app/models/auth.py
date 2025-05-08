import uuid

from pydantic import EmailStr
from sqlmodel import SQLModel, Field

from app.backend.const import Roles


class User(SQLModel, table=True):
    """Модель пользователя магазина"""

    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, description="ID пользователя")
    email: EmailStr = Field(index=True, description="Почта пользователя")
    hashed_password: str = Field(description="Пароль пользователя")
    role_id: int = Field(default=Roles.CLIENT)

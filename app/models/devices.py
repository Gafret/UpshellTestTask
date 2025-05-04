from sqlmodel import SQLModel, Field

from app.utils.validators import DeviceBrand, DeviceName, DevicePrice


class BaseDevice(SQLModel):
    """Корневая модель девайса, используется для формирования дочерних моделей"""

    name: DeviceName = Field(index=True, description="Название девайса")
    brand: DeviceBrand = Field(description="Производитель девайса")
    price: DevicePrice = Field(description="Цена товара")


class Device(BaseDevice, table=True):
    """Модель девайса хранящаяся в БД"""

    __tablename__ = "devices"

    id: int | None = Field(primary_key=True, default=None, description="ID девайса")

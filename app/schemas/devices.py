from pydantic import BaseModel, Field, model_validator

from app.models.devices import BaseDevice
from app.utils.validators import PageField, PageSizeField, OrderDevicePrice, OrderDeviceQuantity, DeviceBrand


class DeviceCreate(BaseDevice):
    """Модель для создания девайса"""

    pass


class DeviceFilterQueryParams(BaseModel):
    """Параметры по которым фильтруются девайсы"""

    brand: DeviceBrand = Field(description="Производитель девайса")
    price_min: int | None = Field(default=None, description="Минимальная цена девайса")
    price_max: int | None = Field(default=None, description="Максимальная цена девайса")
    page: PageField | None = Field(default=1, description="Номер получаемой страницы результатов запроса")
    page_size: PageSizeField | None = Field(default=10, description="Количество элементов на каждой странице")

    @model_validator(mode="after")
    def check_price_range(self):
        if ((self.price_min is not None and self.price_max is not None) and
                self.price_min > self.price_max):
            raise ValueError("Максимальная цена не может быть меньше минимальной цены")
        return self

    @model_validator(mode="after")
    def check_has_at_least_one_field(self):
        values = self.model_dump()
        for k, v in values.items():
            if v is not None:
                return self
        raise ValueError("Должен быть указан хотя бы один параметр фильтрации или пагинации")


class DeviceFilterResult(BaseModel):
    """Результат, получаемый после фильтровки девайсов"""

    items: list[BaseDevice] = Field(description="Элементы, полученные после фильтрации")
    total: int = Field(default=0, description="Итоговое количество, полученных элементов")


class DeviceOrder(BaseDevice):
    """Заказ на некоторый девайс внутри корзины пользователя"""

    price: OrderDevicePrice = Field(description="Цена девайса")
    quantity: OrderDeviceQuantity = Field(description="Кол-во девайсов данной модели")


class UserDeviceCart(BaseModel):
    """Корзина пользователя"""

    items: list[DeviceOrder] = Field(description="Список позиций в корзине покупателя")


class FulfilledDeviceOrder(DeviceOrder):
    """Исполненный заказ на некоторый девайс из корзины"""

    price: float = Field(description="Цена одного девайса данной модели")
    total_price: float = Field(description="Цена за N-ое количество девайсов данной модели")


class CartPurchaseResult(BaseModel):
    """Чек получаемый после покупки корзины"""

    purchased_items: list[FulfilledDeviceOrder] | None = Field(default_factory=list,
                                                               description="Список, купленных позиций")
    total_purchase_price: float | None = Field(default=None, description="Итоговая стоимость")

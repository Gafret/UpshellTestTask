from pydantic import BaseModel, Field, model_validator

from app.backend.const import ErrorTexts
from app.backend.custom_exceptions import FieldValidationException
from app.backend.openapi.schema_examples import DeviceSchemas
from app.models.devices import BaseDevice
from app.utils.validators import PageField, PageSizeField, OrderDevicePrice, OrderDeviceQuantity, DeviceBrand


class DeviceCreate(BaseDevice):
    """Модель для создания девайса"""

    pass

    class Config:
        extra = "forbid"
        json_schema_extra = DeviceSchemas.DEVICE_CREATE


class DeviceFilterQueryParams(BaseModel):
    """Параметры по которым фильтруются девайсы"""

    brand: DeviceBrand | None = Field(default=None, description="Фильтр по бренду")
    price_min: int | None = Field(default=None, description="Минимальная цена")
    price_max: int | None = Field(default=None, description="Максимальная цена")
    page: PageField | None = Field(default=1, description="Номер страницы для пагинации")
    page_size: PageSizeField | None = Field(default=10, description="Количество элементов на странице")

    @model_validator(mode="after")
    def check_price_range(self):
        if ((self.price_min is not None and self.price_max is not None) and
                self.price_min > self.price_max):
            raise FieldValidationException(
                "value_error",
                ErrorTexts.MAX_PRICE_LESS_THAN_MIN_PRICE
            )
        return self

    @model_validator(mode="after")
    def check_has_at_least_one_field(self):
        values = self.model_dump()
        for k, v in values.items():
            if v is not None:
                return self
        raise FieldValidationException(
            "value_error",
            "Должен быть указан хотя бы один параметр фильтрации или пагинации"
        )

    class Config:
        extra = "forbid"


class DeviceFilterResult(BaseModel):
    """Результат, получаемый после фильтровки девайсов"""

    items: list[BaseDevice] = Field(description="Элементы, полученные после фильтрации")
    total: int = Field(default=0, description="Итоговое количество, полученных элементов")

    class Config:
        json_schema_extra = DeviceSchemas.DEVICE_FILTER_RESULT


class DeviceOrder(BaseDevice):
    """Заказ на некоторый девайс внутри корзины пользователя"""

    price: OrderDevicePrice = Field(description="Цена девайса")
    quantity: OrderDeviceQuantity = Field(description="Кол-во девайсов данной модели")

    class Config:
        extra = "forbid"


class UserDeviceCart(BaseModel):
    """Корзина пользователя"""

    items: list[DeviceOrder] = Field(description="Список позиций в корзине покупателя")

    class Config:
        extra = "forbid"
        json_schema_extra = DeviceSchemas.USER_DEVICE_CART


class FulfilledDeviceOrder(DeviceOrder):
    """Исполненный заказ на некоторый девайс из корзины"""

    price: float = Field(description="Цена одного девайса данной модели")
    total_price: float = Field(description="Цена за N-ое количество девайсов данной модели")


class CartPurchaseResult(BaseModel):
    """Чек получаемый после покупки корзины"""

    purchased_items: list[FulfilledDeviceOrder] | None = Field(default_factory=list,
                                                               description="Список, купленных позиций")
    total_purchase_price: float | None = Field(default=None, description="Итоговая стоимость")

    class Config:
        json_schema_extra = DeviceSchemas.CART_PURCHASE_RESULT

import re
from typing import Annotated

from pydantic import AfterValidator

from app.backend.custom_exceptions import FieldValidationException


def validate_password(password: str) -> str:
    """
    Проверяет, что строка длиной от 8 до 20 символов,
    содержит как минимум одну строчную букву,
    одну заглавную букву и одну цифру.
    Разрешены специальные символы.

    Пример:Password123
    """
    if re.match(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[#?!@$%^&*-]*).{8,20}$", password) is None:
        raise FieldValidationException(
            "value_error",
            "Пароль не соответствует требованиям безопасности"
        )
    return password


def validate_login_password(password: str) -> str:
    if len(password) < 8 or len(password) > 20:
        raise FieldValidationException(
            "value_error",
            "Неверный формат пароля"
        )
    return password


def validate_page_number(page: int) -> int:
    if page <= 0:
        raise FieldValidationException("value_error", "Номер страницы должен быть больше 0")
    return page


def validate_page_size(page_size: int) -> int:
    if page_size < 1 or page_size > 100:
        raise FieldValidationException("value_error", "Размер страницы должен быть от 1 до 100")
    return page_size


def validate_cart_price(price: float) -> float:
    if price <= 0:
        raise FieldValidationException("value_error", "Цена товара не может быть отрицательной")
    return price


def validate_order_quantity(quantity: int) -> int:
    if quantity < 1:
        raise FieldValidationException("value_error", "Некорректное количество товара")
    return quantity


def validate_name(name: str | None) -> str:
    if name is None:
        raise FieldValidationException("missing", "Поле name обязательно для заполнения")

    if len(name) < 3 or len(name) > 100:
        raise FieldValidationException("value_error", "Поле name должно содержать от 3 до 100 символов")
    return name


def validate_brand(brand: str | None) -> str:
    if brand is None:
        raise FieldValidationException("missing", "Поле brand обязательно для заполнения")

    if len(brand) < 2 or len(brand) > 50:
        raise FieldValidationException("value_error", "Поле brand должно содержать от 2 до 50 символов")
    return brand


def validate_device_price(price: float) -> float:
    if price < 0.01:
        raise FieldValidationException("value_error", "Цена товара должна быть положительным числом")
    return price


DevicePrice = Annotated[float, AfterValidator(validate_device_price)]
DeviceBrand = Annotated[str, AfterValidator(validate_brand)]
DeviceName = Annotated[str, AfterValidator(validate_name)]

OrderDevicePrice = Annotated[float, AfterValidator(validate_cart_price)]
OrderDeviceQuantity = Annotated[int, AfterValidator(validate_order_quantity)]

PageField = Annotated[int, AfterValidator(validate_page_number)]
PageSizeField = Annotated[int, AfterValidator(validate_page_size)]

PasswordField = Annotated[str, AfterValidator(validate_password)]
LoginPasswordField = Annotated[str, AfterValidator(validate_login_password)]

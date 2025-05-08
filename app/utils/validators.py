import re
from typing import Annotated, LiteralString, Type, Any

from pydantic import AfterValidator, BeforeValidator

from app.backend.const import ErrorTexts
from app.backend.custom_exceptions import FieldValidationException


def length_validation(val: str, min_: int, max_: int) -> bool:
    length = len(val)
    return min_ <= length <= max_


def type_validation_wrapper(obj_type: Type, error_text: LiteralString):
    def checker(val: Any) -> Any:
        if not isinstance(val, obj_type):
            raise FieldValidationException(
                "type_error",
                error_text
            )
        return val
    return checker


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
            ErrorTexts.UNSAFE_PASSWORD,
        )
    return password


def validate_login_password(password: str) -> str:
    if not length_validation(password, 8, 20) or not isinstance(password, str):
        raise FieldValidationException(
            "value_error",
            ErrorTexts.BADLY_FORMATTED_PASSWORD,
        )

    return password


def validate_page_number(page: int) -> int:
    if page <= 0:
        raise FieldValidationException(
            "value_error",
            ErrorTexts.INVALID_PAGE_NUMBER,
        )
    return page


def validate_page_size(page_size: int) -> int:
    if page_size < 1 or page_size > 100:
        raise FieldValidationException(
            "value_error",
            ErrorTexts.INVALID_PAGE_SIZE,
        )
    return page_size


def validate_cart_price(price: float) -> float:
    if price <= 0:
        raise FieldValidationException(
            "value_error",
            ErrorTexts.INVALID_PRICE_IN_CART,
        )
    return price


def validate_order_quantity(quantity: int) -> int:
    if quantity < 1:
        raise FieldValidationException(
            "value_error",
            ErrorTexts.INVALID_QUANTITY,
        )

    return quantity


def validate_name(name: str | None) -> str:
    if not length_validation(name, 3, 100):
        raise FieldValidationException(
            "value_error",
            ErrorTexts.INVALID_NAME
        )
    return name


def validate_brand(brand: str | None) -> str:
    if not length_validation(brand, 2, 50):
        raise FieldValidationException(
            "value_error",
            ErrorTexts.INVALID_BRAND,
        )
    return brand


def validate_token(token: str) -> str:
    if not length_validation(token, 32, 256):
        raise FieldValidationException(
            "value_error",
            ErrorTexts.INVALID_TOKEN,
        )

    return token


def validate_device_price(price: float) -> float:
    if 0 <= price < 0.01:
        raise FieldValidationException(
            "value_error",
            ErrorTexts.INVALID_PURCHASE_PRICE,
        )
    elif price < 0:
        raise FieldValidationException(
            "value_error",
            ErrorTexts.INVALID_PRICE_IN_CART,
        )
    return price


DevicePrice = Annotated[
    float,
    BeforeValidator(type_validation_wrapper(float, ErrorTexts.PRICE_TYPE_ERROR)),
    AfterValidator(validate_device_price),
]

DeviceBrand = Annotated[
    str,
    BeforeValidator(type_validation_wrapper(str, ErrorTexts.GENERAL_WRONG_TYPE)),
    AfterValidator(validate_brand)
]

DeviceName = Annotated[
    str,
    BeforeValidator(type_validation_wrapper(str, ErrorTexts.GENERAL_WRONG_TYPE)),
    AfterValidator(validate_name)
]

OrderDevicePrice = Annotated[
    float,
    BeforeValidator(type_validation_wrapper(float, ErrorTexts.GENERAL_WRONG_TYPE)),
    AfterValidator(validate_cart_price)
]

OrderDeviceQuantity = Annotated[
    int,
    BeforeValidator(type_validation_wrapper(int, ErrorTexts.GENERAL_WRONG_TYPE)),
    AfterValidator(validate_order_quantity)
]

PageField = Annotated[
    int,
    BeforeValidator(type_validation_wrapper(int, ErrorTexts.GENERAL_WRONG_TYPE)),
    AfterValidator(validate_page_number)
]

PageSizeField = Annotated[
    int,
    BeforeValidator(type_validation_wrapper(int, ErrorTexts.GENERAL_WRONG_TYPE)),
    AfterValidator(validate_page_size)
]

PasswordField = Annotated[
    str,
    BeforeValidator(type_validation_wrapper(str, ErrorTexts.BADLY_FORMATTED_PASSWORD)),
    AfterValidator(validate_password),
]

LoginPasswordField = Annotated[
    str,
    BeforeValidator(type_validation_wrapper(str, ErrorTexts.BADLY_FORMATTED_PASSWORD)),
    AfterValidator(validate_login_password)
]

TokenField = Annotated[
    str,
    BeforeValidator(type_validation_wrapper(str, ErrorTexts.GENERAL_WRONG_TYPE)),
    AfterValidator(validate_token)
]

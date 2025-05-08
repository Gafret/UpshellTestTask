from enum import IntEnum


class Roles(IntEnum):
    """Перечисление доступных ролей пользователя"""

    ADMIN = 1
    CLIENT = 2


class ErrorTexts:
    UNSAFE_PASSWORD = "Пароль не соответствует требованиям безопасности."
    BADLY_FORMATTED_PASSWORD = "Неверный формат пароля."
    INVALID_PAGE_NUMBER = "Номер страницы должен быть больше 0."
    INVALID_PAGE_SIZE = "Размер страницы должен быть от 1 до 100."
    INVALID_PRICE_IN_CART = "Цена товара не может быть отрицательной."
    INVALID_QUANTITY = "Некорректное количество товара."
    INVALID_NAME = "Поле name должно содержать от 3 до 100 символов."
    INVALID_BRAND = "Поле brand должно содержать от 2 до 50 символов."
    INVALID_TOKEN = "Токен неверной длины."
    INVALID_PURCHASE_PRICE = "Цена меньше минимальной."
    INVALID_OR_EXPIRED_TOKEN = "Недействительный или истёкший токен."
    INVALID_PASS_OR_EMAIL = "Неверная пара логин и пароль."
    USER_ALREADY_EXISTS = "Пользователь с таким email уже зарегистрирован."
    EMPTY_CART = "Корзина покупок пустая."
    DEVICE_UNAVAILABLE_FOR_PURCHASE = "Товар недоступен для покупки."
    NOT_ENOUGH_DEVICES = "Недостаточно товара на складе."
    PRICE_HAS_CHANGED = "Цена товара изменилась с момента добавления в корзину."
    PRICE_TYPE_ERROR = "Цена товара должна быть положительным числом."
    PAGE_DOESNT_EXIST = "Такой страницы не существует"
    INVALID_TOKEN_TYPE = "Неверный тип токена."
    UNAUTHORIZED_USER = "Неавторизованный пользователь."
    NO_PERMISSION = "Пользователь не имеет прав доступа для этой операции."
    MAX_PRICE_LESS_THAN_MIN_PRICE = "Максимальная цена не может быть меньше минимальной цены."
    GENERAL_WRONG_TYPE = "Неверный тип аттрибута."


class SuccessTexts:
    USER_REGISTERED = "Регистрация прошла успешно."

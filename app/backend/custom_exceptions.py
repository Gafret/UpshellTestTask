from pydantic_core import PydanticCustomError


class FieldValidationException(PydanticCustomError):
    """Ошибка валидации поля с кастомным сообщением"""

    pass

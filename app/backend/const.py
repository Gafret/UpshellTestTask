from enum import IntEnum


class Roles(IntEnum):
    """Перечисление доступных ролей пользователя"""

    ADMIN = 1
    CLIENT = 2

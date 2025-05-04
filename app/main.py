from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from app.backend.exception_handlers import server_exception_handler, http_exception_handler, \
    validation_exception_handler
from app.routers import auth, devices


description = """
# Restful API для магазина техники

## - Устройства
### Вы можете:

* Смотреть устройства
* Покупать девайсы
* Вносить новые позиции в каталог

## - Аутентификация
### Вы можете:

* Зарегистрироваться
* Залогиниться
* Обновить токен
"""

tags_metadata = [
    {
        "name": "auth",
        "description": "Все операции, связанные с пользователями и аутентификацией",
    },
    {
        "name": "devices",
        "description": "Работа с устройствами в каталоге магазина",
    },
]

app = FastAPI(
    title="ShopyShop",
    description=description,
    summary="API лучшего магазина техники",
    version="0.0.1",
    contact={
        "name": "Даниил Лемешко",
    },
    openapi_tags=tags_metadata
)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, server_exception_handler)

app.include_router(auth.router)
app.include_router(devices.router)

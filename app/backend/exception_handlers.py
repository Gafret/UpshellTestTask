from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR

from app.schemas.base import ErrorResponse


async def http_exception_handler(request: Request, exc: HTTPException):
    """Хэндлер любых HTTPException, трансформирующий их в ErrorResponse"""

    content = ErrorResponse(error=exc.detail)

    return JSONResponse(
        content=content.model_dump(),
        status_code=exc.status_code,
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Хэндлер для ошибок валидации Pydantic'а"""

    messages = ""

    for err in exc.errors():
        print(err)
        # так как используется EmailStr для подробной валидации почты,
        # а формат вывода нам нужен собственный, обрабатываем особый случай
        if "email" in err.get("loc") and (err.get("type") == "value_error" or err.get("type") == "string_type"):
            messages += "Некорректный формат электронной почты. "
            continue

        elif err.get("type") == "extra_forbidden":
            messages += f"В {err.get('loc')[0]} переданы избыточные поля. "

        elif err.get("type") == "missing":
            messages += f"В {err.get('loc')[0]} не передано поле '{err.get('loc')[-1]}'. "

        elif err.get("type") == "json_invalid":
            messages += "Неверный формат JSON. "

        else:
            messages += err.pop("msg") + " "

    messages = messages.rstrip()
    content = ErrorResponse(error=messages)

    return JSONResponse(
        content=content.model_dump(),
        status_code=HTTP_400_BAD_REQUEST,
    )


async def server_exception_handler(request: Request, exc: Exception):
    """Хэндлер любых ошибок происходящих на сервере"""

    content = ErrorResponse(error="Произошла ошибка на сервере. Попробуйте позже.")

    return JSONResponse(
        content=content.model_dump(),
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Модель ответа при возникшей ошибке, используемая в хэндлере"""

    error: str

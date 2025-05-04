from typing import Sequence, Any

from sqlalchemy import Select, ScalarResult, Delete
from sqlmodel import Session, SQLModel


class BaseService:
    """Базовый сервис, используемый для наследования от него"""

    def __init__(self, session: Session):
        self.session = session


class BaseDataManager(BaseService):
    """Базовый сервис-репозиторий"""

    def add_one(self, model: SQLModel) -> None:
        self.session.add(model)

    def add_all(self, models: Sequence[SQLModel]) -> None:
        self.session.add_all(models)

    def get_one(self, select_statement: Select) -> ScalarResult:
        return self.session.scalar(select_statement)

    def get_all(self, select_statement: Select) -> ScalarResult[Any]:
        return self.session.scalars(select_statement)

    def delete_one(self, instance: object):
        return self.session.delete(instance)


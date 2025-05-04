from typing import Annotated

from fastapi.params import Depends
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, create_engine

from app.backend.config import config

engine = create_engine(config.database)

SessionFactory = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


def get_session() -> Session:
    """Выдает БД сессию"""

    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()


SessionDependency = Annotated[Session, Depends(get_session)]

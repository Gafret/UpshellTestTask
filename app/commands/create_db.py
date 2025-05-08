from sqlmodel import create_engine, SQLModel

from app.backend.config import config
from app.models.auth import User
from app.models.devices import Device

engine = create_engine(config.database)
SQLModel.metadata.create_all(engine)

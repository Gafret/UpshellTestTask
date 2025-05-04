from sqlmodel import create_engine

from app.backend.config import config
from app.models.auth import User
from app.models.devices import Device

engine = create_engine(config.database)
User.metadata.create_all(engine)
Device.metadata.create_all(engine)

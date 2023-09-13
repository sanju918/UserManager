import enum

from sqlalchemy import Boolean, Column, Integer, String, Enum

from ..db_config import Base
from .mixins import Timestamp


class Role(enum.IntEnum):
    user = 1
    admin = 2


class User(Base, Timestamp):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    role = Column(Enum(Role), nullable=False, default=Role.user)
    is_active = Column(Boolean, default=True, nullable=False)
    password = Column(String, nullable=False)

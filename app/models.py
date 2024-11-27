from datetime import datetime
from unittest.mock import Base

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.expression import false

from .orm.base_model import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    password: Mapped[str] = mapped_column(String(128))

    first_name: Mapped[str] = mapped_column(String(150))
    last_name: Mapped[str] = mapped_column(String(150))
    email: Mapped[str] = mapped_column(String(254), nullable=False)
    is_active: Mapped[bool] = mapped_column(server_default=false())
    is_staff: Mapped[bool] = mapped_column(server_default=false())
    is_superuser: Mapped[bool] = mapped_column(server_default=false())

    data_joined: Mapped[datetime] = mapped_column(server_default=func.now())
    last_login: Mapped[datetime] = mapped_column(server_default=func.now())

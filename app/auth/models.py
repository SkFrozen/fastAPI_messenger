from datetime import datetime

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.expression import false, true

from ..orm.base_model import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(150), nullable=False, unique=True, index=True
    )
    password: Mapped[str] = mapped_column(String(128))

    first_name: Mapped[str] = mapped_column(String(150), nullable=True)
    last_name: Mapped[str] = mapped_column(String(150), nullable=True)
    email: Mapped[str] = mapped_column(String(254), nullable=False)
    is_active: Mapped[bool] = mapped_column(server_default=true())
    is_staff: Mapped[bool] = mapped_column(server_default=false())
    is_superuser: Mapped[bool] = mapped_column(server_default=false())

    data_joined: Mapped[datetime] = mapped_column(server_default=func.now())
    last_login: Mapped[datetime] = mapped_column(server_default=func.now())

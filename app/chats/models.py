from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.functions import func

from app.orm.base_model import BaseModel


class Message(BaseModel):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    sender_id: Mapped[int] = mapped_column(index=True)
    recipient_id: Mapped[int] = mapped_column(index=True)
    message: Mapped[str] = mapped_column(String(4096), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), index=True)

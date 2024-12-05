from datetime import datetime

from app.orm.session import get_session
from app.sockets.schemas import MessageResponseSchema

from ..chats.models import Message


class DatabaseStorage:

    async def save(self, message: MessageResponseSchema):
        async with get_session() as session:
            session.add(
                Message(
                    message=message.message,
                    sender_id=message.sender_id,
                    recipient_id=message.recipient_id,
                    created_at=datetime.fromtimestamp(message.created_at),
                )
            )
            await session.commit()

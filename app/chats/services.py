from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import and_, or_

from app.auth.models import User

from .models import Message


class ChatError(Exception):
    pass


async def create_message(
    session: AsyncSession,
    sender_id: int,
    recipient_id: int,
    message: str,
) -> Message:

    message = Message(sender_id=sender_id, recipient_id=recipient_id, message=message)
    session.add(message)
    await session.commit()
    await session.refresh(message)

    return message


async def get_last_messages(
    session: AsyncSession,
    chat_id: int,
    user_id: int,
    limit: int = 100,
) -> list[Message]:
    chat = await session.get(User, chat_id)
    if chat is None:
        raise ChatError("Chat not found")

    query = (
        select(Message)
        .where(
            or_(
                and_(Message.sender_id == user_id, Message.recipient_id == chat_id),
                and_(Message.recipient_id == user_id, Message.sender_id == chat_id),
            )
        )
        .group_by(Message.id)
        .order_by(Message.created_at.desc())
        .limit(limit)
    )
    result = list((await session.execute(query)).scalars())
    return result


async def update_message(
    session: AsyncSession, chat_id: int, message_id: int, message: str
):
    query = (
        update(Message)
        .where(
            Message.id == message_id,
            Message.recipient_id == chat_id,
        )
        .values(
            message=message,
        )
        .returning(Message.message)
    )
    message = (await session.execute(query)).scalar()

    if message is None:
        raise ChatError("Message not found")

    await session.commit()


async def delete_message(session: AsyncSession, chat_id: int, message_id: int):
    query = delete(Message).where(
        Message.id == message_id,
        Message.recipient_id == chat_id,
    )
    await session.execute(query)
    try:
        await session.commit()
    except IntegrityError:
        raise ChatError("Message not found")

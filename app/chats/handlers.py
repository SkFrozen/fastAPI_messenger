from fastapi import APIRouter, Depends, HTTPException

from app.auth.services.auth import get_user
from app.orm.session import get_session

from .schemas import (
    DeleteMessageSchema,
    MessageSchema,
    NewMessageSchema,
    UpdateMessageSchema,
)
from .services import (
    ChatError,
    create_message,
    delete_message,
    get_last_messages,
    update_message,
)

router = APIRouter(prefix="/{chat_id}/sendMessage", tags=["chats"])


@router.post("", response_model=MessageSchema)
async def create_message_api_view(
    chat_id: int,
    data: NewMessageSchema,
    user=Depends(get_user),
    session=Depends(get_session),
):
    try:
        return await create_message(
            session,
            sender_id=user.id,
            recipient_id=chat_id,
            message=data.message,
        )
    except ChatError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("", response_model=list[MessageSchema])
async def get_last_messages_api_view(
    chat_id: int, session=Depends(get_session), user=Depends(get_user)
):
    try:
        return await get_last_messages(session, chat_id=chat_id, user_id=user.id)
    except ChatError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.patch("/update", response_model=NewMessageSchema)
async def update_message_api_view(
    chat_id: int,
    message_data: UpdateMessageSchema,
    session=Depends(get_session),
):
    try:
        await update_message(
            session,
            chat_id=chat_id,
            message_id=message_data.id,
            message=message_data.message,
        )
    except ChatError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return NewMessageSchema(message=f"Message with id {message_data.id} updated")


@router.delete("/delete", response_model=NewMessageSchema)
async def delete_message_api_view(
    chat_id: int,
    message_data: DeleteMessageSchema,
    session=Depends(get_session),
):
    try:
        await delete_message(session, chat_id=chat_id, message_id=message_data.id)
    except ChatError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return NewMessageSchema(message=f"Message with id {message_data.id} deleted")

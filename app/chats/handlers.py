from fastapi import APIRouter, Depends, HTTPException

from app.auth.services.auth import get_user
from app.orm.session import get_session

from .schemas import MessageSchema, NewMessageSchema
from .services import ChatError, create_message, get_last_messages

router = APIRouter(prefix="/{chat_id}/sendMessage", tags=["chats"])


@router.post("/{chat_id}/sendMessage", response_model=MessageSchema)
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


@router.get("/{chat_id}/lastMessages", response_model=list[MessageSchema])
async def get_last_messages_api_view(
    chat_id: int, session=Depends(get_session), user=Depends(get_user)
):
    try:
        return await get_last_messages(session, chat_id=chat_id, user_id=user.id)
    except ChatError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

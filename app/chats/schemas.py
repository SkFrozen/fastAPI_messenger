from datetime import datetime

from pydantic import BaseModel


class NewMessageSchema(BaseModel):
    message: str


class MessageSchema(BaseModel):
    id: int
    sender_id: int
    recipient_id: int
    message: str
    created_at: datetime


class UpdateMessageSchema(BaseModel):
    id: int
    message: str


class DeleteMessageSchema(BaseModel):
    id: int

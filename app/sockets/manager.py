from datetime import datetime

from fastapi import WebSocket, WebSocketDisconnect
from pydantic import ValidationError
from redis.asyncio import ConnectionPool, Redis

from app.cache import local

from ..settings import settings
from .broadcast import BroadcastManager, LocalBroadcastManager, RedisBroadcastManager
from .schemas import MessageRequestSchema, MessageResponseSchema
from .storages import DatabaseStorage


class ConnectionManager:

    def __init__(self, storage: DatabaseStorage, broadcast: BroadcastManager):
        self._storage = storage
        self._broadcast = broadcast

        self._active_connections: dict[int, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: int) -> None:
        self._active_connections.setdefault(user_id, []).append(websocket)

        await self._broadcast.run_listener(websocket, user_id)

    async def disconnect(self, websocket: WebSocket, user_id: int) -> None:
        try:
            self._active_connections[user_id].remove(websocket)
        except ValueError:
            pass

        await self._broadcast.stop_listener(user_id)

    async def analyze_message(self, data: str, sender_user_id: int) -> None:
        try:
            msg = MessageRequestSchema.model_validate_json(data)
        except ValidationError:
            return

        if msg.type == "message" and msg.recipient_id:
            response = MessageResponseSchema(
                type=msg.type,
                status=msg.status,
                message=msg.message.strip(),
                recipient_id=msg.recipient_id,
                sender_id=sender_user_id,
                created_at=int(datetime.now().timestamp()),
            )

            await self.broadcast(response, msg.recipient_id)
            # save to DB.
            # await self._storage.save(message=response)

    async def broadcast(
        self, message: MessageResponseSchema, recipient_id: int
    ) -> None:
        local_connetions = self._active_connections.get(recipient_id, [])

        if local_connetions:
            for ws in local_connetions:
                try:
                    await ws.send_text(message.model_dump_json())
                except WebSocketDisconnect:
                    pass
        else:
            await self._broadcast.send(message, chat_id=recipient_id)


def get_broadcast_manager() -> BroadcastManager:
    if settings.broadcast_type == "redis":
        pool = ConnectionPool.from_url(
            settings.get_redis_url(),
            max_connections=settings.broadcast_redis_max_connections,
        )
        redis = Redis(connection_pool=pool)
        return RedisBroadcastManager(redis)

    return LocalBroadcastManager()


storage = DatabaseStorage()
broadcast_manager = get_broadcast_manager()
manager = ConnectionManager(storage, broadcast_manager)

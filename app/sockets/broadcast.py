import asyncio
from abc import ABC, abstractmethod
from asyncio import Task

from fastapi import WebSocket, WebSocketDisconnect
from redis.asyncio import Redis, RedisError

from app.sockets.schemas import MessageResponseSchema


class BroadcastManager(ABC):

    @abstractmethod
    async def send(self, message: MessageResponseSchema, chat_id: int):
        pass

    @abstractmethod
    async def run_listener(self, websocket: WebSocket, chat_id: int):
        pass

    @abstractmethod
    async def stop_listener(self, chat_id: int):
        pass


class LocalBroadcastManager(BroadcastManager):
    async def send(self, message: MessageResponseSchema, chat_id: int):
        print(f"{chat_id}: {message}")

    async def run_listener(self, websocket: WebSocket, chat_id: int):
        pass

    async def stop_listener(self, chat_id: int):
        pass


class RedisBroadcastManager(BroadcastManager):

    def __init__(self, redis: Redis):
        self.redis = redis
        self._listener_tasks: dict[int, Task] = {}

    async def send(self, message: MessageResponseSchema, chat_id: int):
        try:
            await self.redis.publish(str(chat_id), message.model_dump_json())
        except RedisError as e:
            print(e)

    async def run_listener(self, websocket: WebSocket, chat_id: int):
        async def async_listener():
            pubsub = self.redis.pubsub()
            await pubsub.subscribe(str(chat_id))
            try:
                while True:
                    msg = await pubsub.get_message(
                        ignore_subscribe_messages=True, timeout=5
                    )
                    if msg is None or msg["type"] != "message" or msg["data"] is None:
                        continue
                    try:
                        await websocket.send_text(msg["data"].decode("utf-8"))
                    except WebSocketDisconnect:
                        return
            finally:
                await pubsub.unsubscribe()
                await pubsub.close()

        self._listener_tasks[chat_id] = asyncio.create_task(async_listener())

    async def stop_listener(self, chat_id: int):
        task = self._listener_tasks.get(chat_id)
        if task:
            task.cancel()

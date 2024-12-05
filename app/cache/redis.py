import pickle
from typing import Any, Optional

from redis.asyncio import ConnectionPool, Redis

from ..settings import settings
from .base import AbstractCache


class RedisCache(AbstractCache):
    """Redis cache."""

    def __init__(self, url: str, max_connections: int = 5) -> None:
        self._pool = ConnectionPool.from_url(
            url=url,
            socket_timeout=2,
            socket_connect_timeout=2,
            max_connections=max_connections,
        )
        self._redis = Redis(connection_pool=self._pool)

    async def get(self, key: str) -> Optional[Any]:

        if value := await self._redis.get(key):
            return pickle.loads(value)
        return None

    async def set(self, key: str, value: Any, expire: int = 0) -> None:
        await self._redis.set(
            key, pickle.dumps(value), ex=expire if expire > 0 else None
        )

    async def delete(self, key: str) -> None:
        await self._redis.delete(key)

    async def delete_namespace(self, prefix: str) -> None:
        async for key in self._redis.scan_iter(f"{prefix}*"):
            await self._redis.delete(key)

    async def clear(self) -> None:
        await self._redis.flushdb(asynchronous=True)


redis_cache = RedisCache(
    settings.get_redis_url(), max_connections=settings.redis_max_connections
)

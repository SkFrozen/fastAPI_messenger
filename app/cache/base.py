from abc import ABC, abstractmethod
from typing import Any, Optional


class AbstractCache(ABC):
    """An Abstract class for implementing the cache."""

    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """Get the value of the key."""
        pass

    @abstractmethod
    async def set(self, key: str, value: Any) -> None:
        """Set the value of the key. Set time to live."""
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        """Delete the value by key."""
        pass

    @abstractmethod
    async def delete_namespace(self, prefix: str) -> None:
        """Deletes all keys starting with the prefix"""
        pass

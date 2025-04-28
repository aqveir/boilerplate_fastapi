""" Import the required modules """
import abc
from typing import Optional, Tuple

class ICache(abc.ABC):
    """
    Interface for cache backend.

    This interface defines the methods that any cache backend should 
    implement. It is used to create a cache manager that can work with
    different cache backends.
    """

    @abc.abstractmethod
    async def get_with_ttl(self, key: str) -> Tuple[int, Optional[bytes]]:
        """Get a value from the cache by key, along with its TTL."""
        raise NotImplementedError

    @abc.abstractmethod
    async def get(self, key: str) -> Optional[bytes]:
        """Get a value from the cache by key."""
        raise NotImplementedError

    @abc.abstractmethod
    async def set(self, key: str, value: bytes, expire: Optional[int] = None) -> None:
        """Set a value in the cache with an optional expiration time."""
        raise NotImplementedError

    @abc.abstractmethod
    async def clear(self, namespace: Optional[str] = None, key: Optional[str] = None) -> int:
        """Clear the cache for a specific namespace or key."""
        raise NotImplementedError

import abc
from typing import Any, Dict, Optional

from redis.client import Redis

from backoff import backoff


class BaseStorage(abc.ABC):
    """Abstract state storage.

    Allows saving and retrieving state information.
    The actual storage implementation can vary, for example, it could
    use a database or a distributed file storage.
    """

    @abc.abstractmethod
    def save_state(self, state: Dict[str, Any]) -> None:
        """Save state to the storage."""

    @abc.abstractmethod
    def retrieve_state(self, key: str) -> Optional[Any]:
        """Retrieve state from the storage."""


class RedisStorage(BaseStorage):
    """
    Storage implementation that uses Redis.
    """

    def __init__(self, redis_adapter: Redis) -> None:
        self.redis_adapter = redis_adapter

    def save_state(self, state: Dict[str, Any]) -> None:
        """Save state to the Redis storage."""

        self.redis_adapter.set(state['key'], state['value'])

    def retrieve_state(self, key: str) -> Optional[Any]:
        """Retrieve state from the Redis storage."""

        return self.redis_adapter.get(key)


class State:
    """Class for managing states."""

    def __init__(self, storage: BaseStorage) -> None:
        self.storage = storage

    @backoff()
    def set_state(self, key: str, value: Any) -> None:
        """
        Set the state for a specific key.

        :param key:
        :param value:

        :return: None
        """
        self.storage.save_state({
            'key': key,
            'value': value
        })

    @backoff()
    def get_state(self, key: str, default: Any = None) -> Optional[Any]:
        """
        Get the state for a specific key.

        :param key:
        :param default: If nothing found by key returns value

        :return: Optional[Any]
        """

        result = self.storage.retrieve_state(key)
        if default is not None and result is None:
            return default

        return result.decode() if result else None

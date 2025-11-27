import time
from typing import Any, Optional


class DataCache:
    """
    Simple in-memory caching system with optional TTL support.
    """

    def __init__(self):
        self._store: dict[str, tuple[Any, Optional[float]]] = {}

    def set(self, key: str, value: Any, timeout: Optional[int] = None) -> None:
        expire_at = time.time() + timeout if timeout else None
        self._store[key] = (value, expire_at)

    def get(self, key: str, default: Any = None) -> Any:
        item = self._store.get(key)
        if not item:
            return default

        value, expire_at = item

        if expire_at and time.time() > expire_at:
            del self._store[key]
            return default

        return value

    def clear(self):
        self._store.clear()
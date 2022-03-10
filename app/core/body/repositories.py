from typing import Any

from app.core.body.exceptions import BodyNotFound


class BodyRepository:
    def __init__(self, *, storage: dict[str, Any]) -> None:
        self._storage = storage

    def save_body(self, key: str, body: dict[Any, Any]) -> None:
        self._storage[key] = body

    def get_body(self, key: str) -> dict[Any, Any]:
        body = self._storage.get(key)
        if body is None:
            raise BodyNotFound(key=key)
        return body

    def delete_body(self, key: str) -> None:
        del self._storage[key]

    def get_count_bodies(self) -> int:
        return len(self._storage)

    def get_duplicates_bodies(self) -> int:
        return sum(
            v["duplicates"] for v in filter(lambda o: o["duplicates"] > 1, self._storage.values())
        )

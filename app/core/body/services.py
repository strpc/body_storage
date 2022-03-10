import base64
from typing import Any, Union

from loguru import logger

from app.core.body.exceptions import BodyNotFound
from app.core.body.repositories import BodyRepository


class BodyService:
    def __init__(self, *, repository: BodyRepository) -> None:
        self._repository = repository

    def save_body(self, body: dict[Any, Any]) -> str:
        key = self._get_body_key(body)

        is_exist_body = self.is_exist_body(key)
        if is_exist_body:
            body = self.get_body(key)
            body["duplicates"] += 1
        else:
            body["duplicates"] = 1

        self._repository.save_body(key=key, body=body)
        logger.debug("body={} was saved with key={}", body, key)
        return key

    def get_body(self, key: str) -> dict[Any, Any]:
        return self._repository.get_body(key=key)

    def update_body(self, key: str, body: dict[Any, Any]) -> str:
        is_exist_body = self.is_exist_body(key=key)
        if not is_exist_body:
            raise BodyNotFound(key=key)

        body["duplicates"] = 1
        self._repository.save_body(key=key, body=body)
        logger.debug("body={} was updated")
        return key

    def delete_body(self, key: str) -> None:
        is_exist_body = self.is_exist_body(key=key)
        if not is_exist_body:
            raise BodyNotFound(key=key)
        return self._repository.delete_body(key=key)

    def is_exist_body(self, key: str) -> bool:
        try:
            _ = self._repository.get_body(key=key)
            return True
        except BodyNotFound:
            return False

    @staticmethod
    def _get_body_key(body: dict[Any, Any]) -> str:
        key = b"".join(f"{k}{v}".encode() for k, v in body.items())
        encoded_key = base64.b64encode(key)
        return encoded_key.decode("utf-8")

    def get_percent_duplicates_bodies(self) -> Union[int, float]:
        count = self._repository.get_count_bodies()
        duplicate = self._repository.get_duplicates_bodies()
        if duplicate == 0:
            return 0
        return count / duplicate * 100

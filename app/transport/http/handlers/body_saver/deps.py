from typing import Any

from fastapi import Depends, Request

from app.core.body.repositories import BodyRepository
from app.core.body.services import BodyService


def get_body_storage(request: Request) -> dict[str, Any]:
    return request.app.state.storage


def get_body_repository(storage: dict[str, Any] = Depends(get_body_storage)) -> BodyRepository:
    return BodyRepository(storage=storage)


def get_body_service(repository: BodyRepository = Depends(get_body_repository)) -> BodyService:
    return BodyService(repository=repository)

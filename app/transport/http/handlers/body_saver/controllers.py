from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.core.body.exceptions import BodyNotFound
from app.core.body.services import BodyService
from app.transport.http.handlers.body_saver.deps import get_body_service
from app.transport.http.handlers.body_saver.schemas import (
    BodySchema,
    DuplicatesBodiesResponse,
    GetBodyResponse,
    SavedBodyResponse,
)

router = APIRouter(tags=["Body Saver"])


@router.post(
    "/body",
    response_model=SavedBodyResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_body(
    body: BodySchema,
    body_service: BodyService = Depends(get_body_service),
) -> SavedBodyResponse:
    key = body_service.save_body(body.dict())
    return SavedBodyResponse(key=key)


@router.get(
    "/body",
    response_model=GetBodyResponse,
    status_code=status.HTTP_200_OK,
)
async def get_body(
    key: str,
    body_service: BodyService = Depends(get_body_service),
) -> GetBodyResponse:
    try:
        body = body_service.get_body(key)
    except BodyNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    return GetBodyResponse.parse_obj(body)


@router.put(
    "/body/{key}",
    response_model=SavedBodyResponse,
    status_code=status.HTTP_200_OK,
)
async def update_key(
    key: str,
    body: BodySchema,
    body_service: BodyService = Depends(get_body_service),
) -> SavedBodyResponse:
    try:
        key = body_service.update_body(key, body.dict())
    except BodyNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    return SavedBodyResponse(key=key)


@router.delete(
    "/body/{key}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def delete_key(key: str, body_service: BodyService = Depends(get_body_service)) -> None:
    try:
        body_service.delete_body(key)
    except BodyNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error


@router.get(
    "/statistic",
    status_code=status.HTTP_200_OK,
    response_model=DuplicatesBodiesResponse,
)
async def get_statistic(
    body_service: BodyService = Depends(get_body_service),
) -> DuplicatesBodiesResponse:
    percent_duplicates = body_service.get_percent_duplicates_bodies()
    return DuplicatesBodiesResponse(percent_duplicates=percent_duplicates)

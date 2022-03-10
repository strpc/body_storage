from fastapi import APIRouter, Response, status

router = APIRouter(tags=["Service Routes"])


@router.get("/healthcheck")
async def healthcheck() -> Response:
    return Response(status_code=status.HTTP_200_OK)

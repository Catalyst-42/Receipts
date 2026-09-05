from typing import Annotated

from fastapi import Depends, Path
from fastapi.responses import StreamingResponse
from fastapi.routing import APIRouter

from src.core.schemes import Count, ErrorResponse
from src.crpt.dependencies import get_crpt_service
from src.crpt.schemes import Crpt, CrptId
from src.crpt.service import CrptService

router = APIRouter(prefix="/crpt", tags=["CRPT"])


@router.get(
    "/stats/count",
    response_model=Count,
)
async def get_crpt_count(
    receipt_service: CrptService = Depends(get_crpt_service),
) -> Count:
    """Returns total count of crpt records in database"""
    return await receipt_service.get_count()


@router.get("/export")
async def download_export(
    crpt_service: CrptService = Depends(get_crpt_service),
) -> StreamingResponse:
    """Returns dump of all crpt QR codes"""
    result = await crpt_service.export()
    return result


@router.get(
    "/{crpt_id}",
    response_model=Crpt,
    responses={
        404: {"model": ErrorResponse, "description": "Crpt record not found"},
    },
)
async def get_crpt(
    request: Annotated[CrptId, Path()],
    crpt_service: CrptService = Depends(get_crpt_service),
) -> Crpt:
    """Returns crpt record by its unique id"""
    result = await crpt_service.get_by_id(request.crpt_id)
    return result

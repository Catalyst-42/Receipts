from typing import Annotated

from fastapi import Depends, Path
from fastapi.responses import StreamingResponse
from fastapi.routing import APIRouter

from src.users.dependencies import get_user
from src.users.schemes import User
from src.core.schemes import ErrorResponse
from src.crpt.dependencies import get_crpt_service
from src.crpt.schemes import Crpt, CrptId, CrptStats
from src.crpt.service import CrptService

router = APIRouter(prefix="/crpt", tags=["CRPT"])


@router.get(
    "/stats",
    response_model=CrptStats,
)
async def get_crpt_stats(
    crpt_service: CrptService = Depends(get_crpt_service),
) -> CrptStats:
    """Returns statistics for CRPT records."""
    return await crpt_service.get_stats()


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

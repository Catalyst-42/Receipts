from typing import Annotated

from fastapi import Depends, Path
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.core.schemes import ErrorResponse
from src.nds.schemes import GetNdsByIdRequest, Nds, NdsList
from src.nds.service import NdsService

router = APIRouter(prefix="/nds", tags=["Nds"])


def get_measures_service(db: AsyncSession = Depends(get_db)):
    return NdsService(db)


@router.get("/", response_model=NdsList)
async def get_nds_rates(
    nds_service: NdsService = Depends(get_measures_service),
) -> NdsList:
    """Returns all directory of nds rates"""
    result = await nds_service.get_all()
    return result


@router.get(
    "/{nds_id}",
    response_model=Nds,
    responses={
        404: {"model": ErrorResponse, "description": "Nds rate not found"},
    },
)
async def get_nds_rate(
    request: Annotated[GetNdsByIdRequest, Path()],
    nds_service: NdsService = Depends(get_measures_service),
) -> Nds:
    """Finds nds rate by its id"""
    result = await nds_service.get_by_id(request.nds_id)
    return result

from typing import Annotated

from fastapi import Depends, Path
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.core.schemes import Count, ErrorResponse
from src.measures.schemes import MeasureId, Measure, MeasureList
from src.measures.service import MeasuresService

router = APIRouter(prefix="/measures", tags=["Measures"])


def get_measures_service(db: AsyncSession = Depends(get_db)):
    return MeasuresService(db)


@router.get("/", response_model=MeasureList)
async def get_measure_types(
    measures_service: MeasuresService = Depends(get_measures_service),
) -> MeasureList:
    """Returns all directory of item measures"""
    result = await measures_service.get_all()
    return result


@router.get(
    "/stats/count",
    response_model=Count,
)
async def get_receipts_count(
    measures_service: MeasuresService = Depends(get_measures_service),
) -> Count:
    """Returns total count of measure types in database"""
    return await measures_service.get_count()


@router.get(
    "/{measure_id}",
    response_model=Measure,
    responses={
        404: {"model": ErrorResponse, "description": "Measure not found"},
    },
)
async def get_measure(
    request: Annotated[MeasureId, Path()],
    measures_service: MeasuresService = Depends(get_measures_service),
) -> Measure:
    """Finds measure by its id"""
    result = await measures_service.get_by_id(request.measure_id)
    return result

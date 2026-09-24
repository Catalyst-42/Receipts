from typing import Annotated

from fastapi import Depends, Path
from fastapi.routing import APIRouter

from src.core.schemes import ErrorResponse
from src.operators.dependencies import get_operators_service
from src.operators.schemes import Operator, OperatorId, OperatorsStats
from src.operators.service import OperatorsService

router = APIRouter(prefix="/operators", tags=["Operators"])


@router.get(
    "/stats",
    response_model=OperatorsStats,
)
async def get_operators_stats(
    operators_service: OperatorsService = Depends(get_operators_service),
) -> OperatorsStats:
    """Returns statistics for operator records."""
    return await operators_service.get_stats()


@router.get(
    "/{operator_id}",
    response_model=Operator,
    responses={
        404: {"model": ErrorResponse, "description": "Operator not found"},
    },
)
async def get_operator(
    request: Annotated[OperatorId, Path()],
    operators_service: OperatorsService = Depends(get_operators_service),
) -> Operator:
    """Returns operator by its unique"""
    result = await operators_service.get_by_id(request.operator_id)
    return result

from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi_filter import FilterDepends
from fastapi_pagination import Page

from src.operators.dependencies import get_operators_service
from src.operators.filters import OperatorsFilters
from src.operators.schemes import Operator
from src.operators.service import OperatorsService
from src.users.dependencies import get_admin
from src.users.schemes import User

router = APIRouter(prefix="/admin/operators", tags=["Admin"])


@router.get("/")
async def get_operators(
    admin: User = Depends(get_admin),
    filters: OperatorsFilters = FilterDepends(OperatorsFilters),
    operators_service: OperatorsService = Depends(get_operators_service),
) -> Page[Operator]:
    """Returns list of operators"""
    return await operators_service.get(filters)

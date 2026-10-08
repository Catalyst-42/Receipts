from typing import Annotated, Any

from fastapi import Depends, Query
from fastapi.responses import StreamingResponse
from fastapi.routing import APIRouter
from fastapi_filter import FilterDepends
from fastapi_pagination import Page

from src.crpt.dependencies import get_crpt_service
from src.crpt.filters import CrptFilters
from src.crpt.schemes import Crpt
from src.crpt.service import CrptService
from src.receipts.schemes import FiscalFields
from src.users.dependencies import get_admin
from src.users.schemes import User

router = APIRouter(prefix="/admin/crpt", tags=["Admin"])


@router.get("/export")
async def download_export(
    admin: User = Depends(get_admin),
    crpt_service: CrptService = Depends(get_crpt_service),
) -> StreamingResponse:
    """Returns dump of all crpt QR codes"""
    return await crpt_service.export()


@router.get("/from-crpt-api", response_model=dict)
async def get_from_crpt_api(
    fiscal_fields: Annotated[FiscalFields, Query()],
    admin: User = Depends(get_admin),
    crpt_service: CrptService = Depends(get_crpt_service),
) -> dict[str, Any]:
    """Returns original CRPT response by receipt"""
    return await crpt_service.get_from_crpt_api(fiscal_fields)


@router.get("/")
async def get_crpt(
    admin: User = Depends(get_admin),
    filters: CrptFilters = FilterDepends(CrptFilters),
    crpt_service: CrptService = Depends(get_crpt_service),
) -> Page[Crpt]:
    """Returns list of crpt records"""
    return await crpt_service.get(filters)

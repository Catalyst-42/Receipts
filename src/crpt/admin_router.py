from fastapi import Depends
from fastapi.responses import StreamingResponse
from fastapi.routing import APIRouter
from fastapi_filter import FilterDepends
from fastapi_pagination import Page

from src.crpt.dependencies import get_crpt_service
from src.crpt.filters import CrptFilters
from src.crpt.schemes import Crpt
from src.crpt.service import CrptService
from src.users.dependencies import get_admin
from src.users.schemes import User

router = APIRouter(prefix="/admin/crpt", tags=["Admin"])


@router.get("/export")
async def download_export(
    admin: User = Depends(get_admin),
    crpt_service: CrptService = Depends(get_crpt_service),
) -> StreamingResponse:
    """Returns dump of all crpt QR codes"""
    result = await crpt_service.export()
    return result


@router.get("/")
async def get_crpt(
    admin: User = Depends(get_admin),
    filters: CrptFilters = FilterDepends(CrptFilters),
    crpt_service: CrptService = Depends(get_crpt_service),
) -> Page[Crpt]:
    """Returns list of crpt records"""
    return await crpt_service.get(filters)

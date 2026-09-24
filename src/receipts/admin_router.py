from fastapi import Depends
from fastapi_filter import FilterDepends
from fastapi_pagination import Page
from fastapi.routing import APIRouter

from src.receipts.dependencies import get_receipts_service
from src.receipts.service import ReceiptsService
from src.users.dependencies import get_admin
from src.users.schemes import User
from src.receipts.filters import ReceiptsFilters
from src.receipts.schemes import Receipt

router = APIRouter(prefix="/admin/receipts", tags=["Admin"])


@router.get("/")
async def get_receipts(
    admin: User = Depends(get_admin),
    filters: ReceiptsFilters = FilterDepends(ReceiptsFilters),
    receipts_service: ReceiptsService = Depends(get_receipts_service),
) -> Page[Receipt]:
    """Returns list of receipts"""
    return await receipts_service.get(filters)

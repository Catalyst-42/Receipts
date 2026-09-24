from fastapi import Depends
from fastapi.responses import StreamingResponse
from fastapi.routing import APIRouter
from fastapi_filter import FilterDepends
from fastapi_pagination import Page

from src.retailers.dependencies import get_retailers_service
from src.retailers.filters import RetailersFilters
from src.retailers.schemes import Retailer
from src.retailers.service import RetailersService
from src.users.dependencies import get_admin
from src.users.schemes import User

router = APIRouter(prefix="/admin/retailers", tags=["Admin"])


@router.get("/")
async def get_retailers(
    admin: User = Depends(get_admin),
    filters: RetailersFilters = FilterDepends(RetailersFilters),
    retailers_service: RetailersService = Depends(get_retailers_service),
) -> Page[Retailer]:
    """Returns list of retailers records"""
    return await retailers_service.get(filters)

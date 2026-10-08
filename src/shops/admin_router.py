from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi_filter import FilterDepends
from fastapi_pagination import Page

from src.shops.dependencies import get_shops_service
from src.shops.filters import ShopsFilters
from src.shops.schemes import Shop
from src.shops.service import ShopsService
from src.users.dependencies import get_admin
from src.users.schemes import User

router = APIRouter(prefix="/admin/shops", tags=["Admin"])


@router.get("/")
async def get_shops(
    admin: User = Depends(get_admin),
    filters: ShopsFilters = FilterDepends(ShopsFilters),
    shops_service: ShopsService = Depends(get_shops_service),
) -> Page[Shop]:
    """Returns list of shops"""
    return await shops_service.get(filters)

from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi_filter import FilterDepends
from fastapi_pagination import Page

from src.shops.dependencies import get_shops_service
from src.shops.filters import ShopsFilters
from src.shops.schemes import Address, Geolocation, Shop
from src.shops.service import ShopsService
from src.users.dependencies import get_admin
from src.users.schemes import User

router = APIRouter(prefix="/admin/shops", tags=["Admin"])


@router.post(
    "/clean-addres",
    response_model=Geolocation,
)
async def get_clean_address(
    address: Address,
    admin: User = Depends(get_admin),
    shop_service: ShopsService = Depends(get_shops_service),
) -> Geolocation:
    """Returns cleaned address"""
    return await shop_service.clean_address(address.address)


@router.get("/")
async def get_shops(
    admin: User = Depends(get_admin),
    filters: ShopsFilters = FilterDepends(ShopsFilters),
    shops_service: ShopsService = Depends(get_shops_service),
) -> Page[Shop]:
    """Returns list of shops"""
    return await shops_service.get(filters)

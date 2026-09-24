from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi_filter import FilterDepends
from fastapi_pagination import Page

from src.items.dependencies import get_items_service
from src.items.filters import ItemsFilters
from src.items.schemes import Item
from src.items.service import ItemsService
from src.users.dependencies import get_admin
from src.users.schemes import User

router = APIRouter(prefix="/admin/items", tags=["Admin"])


@router.get("/")
async def get_items(
    admin: User = Depends(get_admin),
    filters: ItemsFilters = FilterDepends(ItemsFilters),
    items_service: ItemsService = Depends(get_items_service),
) -> Page[Item]:
    """Returns list of items"""
    return await items_service.get(filters)

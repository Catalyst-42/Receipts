from typing import Annotated

from fastapi import Depends, Path
from fastapi.routing import APIRouter

from src.core.schemes import ErrorResponse
from src.items.schemes import ItemList
from src.shops.dependencies import get_shops_service
from src.shops.schemes import Shop, ShopId, ShopsStats
from src.shops.service import ShopsService

router = APIRouter(prefix="/shops", tags=["Shops"])


@router.get(
    "/stats",
    response_model=ShopsStats,
)
async def get_shops_stats(
    shop_service: ShopsService = Depends(get_shops_service),
) -> ShopsStats:
    """Returns statistics for shop records."""
    return await shop_service.get_stats()


@router.get(
    "/{shop_id}/items",
    response_model=ItemList,
    responses={
        404: {"model": ErrorResponse, "description": "Shop not found"},
    },
)
async def get_shop_items(
    request: Annotated[ShopId, Path()],
    shop_service: ShopsService = Depends(get_shops_service),
) -> ItemList:
    """Returns all items sold in this shop"""
    result = await shop_service.get_items(request.shop_id)
    return result


@router.get(
    "/{shop_id}",
    response_model=Shop,
    responses={
        404: {"model": ErrorResponse, "description": "Shop not found"},
    },
)
async def get_shop(
    request: Annotated[ShopId, Path()],
    shop_service: ShopsService = Depends(get_shops_service),
) -> Shop:
    """Returns shop by its unique id"""
    result = await shop_service.get_by_id(request.shop_id)
    return result

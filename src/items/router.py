from typing import Annotated

from fastapi import Depends, Path
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.core.schemes import Average, Count, CountDistinct, ErrorResponse, Median
from src.items.schemes import Item, ItemId
from src.items.service import ItemsService

router = APIRouter(prefix="/items", tags=["Items"])


def get_items_service(db: AsyncSession = Depends(get_db)):
    return ItemsService(db)


@router.get(
    "/stats/count",
    response_model=Count,
)
async def get_items_count(
    items_service: ItemsService = Depends(get_items_service),
) -> Count:
    """Returns total count of items in receipts"""
    return await items_service.get_count()


@router.get(
    "/stats/count-distinct",
    response_model=CountDistinct,
)
async def get_unique_items_count(
    items_service: ItemsService = Depends(get_items_service),
) -> CountDistinct:
    """Returns total count of unique items in receipts"""
    return await items_service.get_count_distinct()


@router.get(
    "/stats/average-price",
    response_model=Average,
)
async def get_item_average_price(
    items_service: ItemsService = Depends(get_items_service),
) -> Average:
    """Returns average (mean) item price"""
    return await items_service.get_avg_price()


@router.get(
    "/stats/median-price",
    response_model=Median,
)
async def get_item_mean_price(
    items_service: ItemsService = Depends(get_items_service),
) -> Median:
    """Returns median item price"""
    return await items_service.get_median_price()


@router.get(
    "/{item_id}",
    response_model=Item,
    responses={
        404: {"model": ErrorResponse, "description": "Item not found"},
    },
)
async def get_item(
    request: Annotated[ItemId, Path()],
    items_service: ItemsService = Depends(get_items_service),
) -> Item:
    """Returns item by its unique id"""
    result = await items_service.get_by_id(request.item_id)
    return result

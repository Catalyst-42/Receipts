from typing import Annotated

from fastapi import Depends, Path
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.core.schemes import Count, ErrorResponse
from src.items.schemes import Item, ItemId, ItemList
from src.items.service import ItemsService
from src.receipts.schemes import ReceiptId

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
    """Returns total count of receipts items in database"""
    return await items_service.get_count()


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

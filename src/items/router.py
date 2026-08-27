from typing import Annotated

from fastapi import Depends, Path
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.core.schemes import ErrorResponse
from src.items.schemes import Item, ItemId
from src.items.service import ItemsService

router = APIRouter(prefix="/items", tags=["Items"])


def get_items_service(db: AsyncSession = Depends(get_db)):
    return ItemsService(db)


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

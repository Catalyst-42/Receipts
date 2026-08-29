from typing import Annotated

from fastapi import Depends, Path
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.core.schemes import ErrorResponse
from src.shops.schemes import Shop, ShopId
from src.shops.service import ShopsService
from src.core.schemes import Count

router = APIRouter(prefix="/shops", tags=["Shops"])


def get_shops_service(db: AsyncSession = Depends(get_db)):
    return ShopsService(db)


@router.get(
    "/stats/count",
    response_model=Count,
)
async def get_receipts_count(
    shop_service: ShopsService = Depends(get_shops_service),
) -> Count:
    """Returns total count of shops in database"""
    return await shop_service.get_count()


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

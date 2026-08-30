from typing import Annotated

from fastapi import Depends, Path
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.core.schemes import ErrorResponse
from src.retailers.schemes import Retailer, RetailerId
from src.retailers.service import RetailersService
from src.core.schemes import Count
from src.items.schemes import ItemList

router = APIRouter(prefix="/retailers", tags=["Retailers"])


def get_retailers_service(db: AsyncSession = Depends(get_db)):
    return RetailersService(db)


@router.get(
    "/stats/count",
    response_model=Count,
)
async def get_retailers_count(
    retailers_service: RetailersService = Depends(get_retailers_service),
) -> Count:
    """Returns total count of retailers in database"""
    return await retailers_service.get_count()


@router.get(
    "/{retailer_id}/items",
    response_model=ItemList,
    responses={
        404: {"model": ErrorResponse, "description": "Retailer not found"},
    },
)
async def get_retailer(
    request: Annotated[RetailerId, Path()],
    retailers_service: RetailersService = Depends(get_retailers_service),
) -> ItemList:
    """Returns all item by retailers unique id"""
    result = await retailers_service.get_items(request.retailer_id)
    return result


@router.get(
    "/{retailer_id}",
    response_model=Retailer,
    responses={
        404: {"model": ErrorResponse, "description": "Retailer not found"},
    },
)
async def get_retailer(
    request: Annotated[RetailerId, Path()],
    retailers_service: RetailersService = Depends(get_retailers_service),
) -> Retailer:
    """Returns retailer by its unique id"""
    result = await retailers_service.get_by_id(request.retailer_id)
    return result

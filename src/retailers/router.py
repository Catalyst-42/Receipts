from typing import Annotated

from fastapi import Depends, Path
from fastapi.routing import APIRouter

from src.core.schemes import ErrorResponse
from src.items.schemes import ItemList
from src.retailers.dependencies import get_retailers_service
from src.retailers.schemes import Retailer, RetailerId, RetailersStats
from src.retailers.service import RetailersService

router = APIRouter(prefix="/retailers", tags=["Retailers"])


@router.get(
    "/stats",
    response_model=RetailersStats,
)
async def get_retailers_stats(
    retailers_service: RetailersService = Depends(get_retailers_service),
) -> RetailersStats:
    """Returns statistics for retailer records."""
    return await retailers_service.get_stats()


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

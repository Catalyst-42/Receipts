from typing import Annotated

from fastapi import Depends, Path, Query
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.core.schemes import Count, ErrorResponse, Total
from src.receipts.schemes import FiscalFields, Receipt, ReceiptId
from src.receipts.service import ReceiptsService
from src.items.schemes import ItemList

router = APIRouter(prefix="/receipts", tags=["Receipts"])


def get_receipts_service(db: AsyncSession = Depends(get_db)):
    return ReceiptsService(db)


@router.get(
    "/stats/count",
    response_model=Count,
)
async def get_receipts_count(
    receipt_service: ReceiptsService = Depends(get_receipts_service),
) -> Count:
    """Returns total count of receipts in database"""
    result = await receipt_service.get_count()
    return result


@router.get(
    "/stats/total",
    response_model=Total,
)
async def get_receipts_total(
    receipt_service: ReceiptsService = Depends(get_receipts_service),
) -> Total:
    """Returns total sum of prices of receipts in database"""
    result = await receipt_service.get_total()
    return result


@router.get(
    "/by-fiscal-fields",
    response_model=FiscalFields,
    responses={
        404: {"model": ErrorResponse, "description": "Receipt not found"},
        503: {"model": ErrorResponse, "description": "CRPT API not available"},
    },
)
async def get_receipt_by_fiscal_fields(
    request: Annotated[FiscalFields, Query()],
    receipt_service: ReceiptsService = Depends(get_receipts_service),
) -> Receipt:
    """Returns full recepie info by fiscal data"""
    result = await receipt_service.get_by_fiscal_fields(request)
    return result


@router.get(
    "/{receipt_id}/items",
    response_model=ItemList,
    responses={
        404: {"model": ErrorResponse, "description": "Receipt not found"},
    },
)
async def get_receipt_by_id(
    request: Annotated[ReceiptId, Path()],
    receipt_service: ReceiptsService = Depends(get_receipts_service),
) -> ItemList:
    """Returns items of receipt by receipt unique id"""
    result = await receipt_service.get_items(request.receipt_id)
    return result


@router.get(
    "/{receipt_id}",
    response_model=Receipt,
    responses={
        404: {"model": ErrorResponse, "description": "Receipt not found"},
    },
)
async def get_receipt_by_id(
    request: Annotated[ReceiptId, Path()],
    receipt_service: ReceiptsService = Depends(get_receipts_service),
) -> Receipt:
    """Returns receipt info by its unique id"""
    result = await receipt_service.get_by_id(request.receipt_id)
    return result

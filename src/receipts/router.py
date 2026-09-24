from typing import Annotated

from fastapi import Depends, Path, Query
from fastapi.routing import APIRouter

from src.core.schemes import ErrorResponse
from src.items.schemes import ItemList
from src.receipts.dependencies import get_receipts_service
from src.receipts.schemes import FiscalFields, Receipt, ReceiptId, ReceiptsStats
from src.receipts.service import ReceiptsService

router = APIRouter(prefix="/receipts", tags=["Receipts"])


@router.get("/stats", response_model=ReceiptsStats)
async def get_receipts_stats(
    receipt_service: ReceiptsService = Depends(get_receipts_service),
) -> ReceiptsStats:
    """Returns statistics for receipt records."""
    return await receipt_service.get_stats()


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
    return await receipt_service.get_by_fiscal_fields(request)


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
    return await receipt_service.get_items(request.receipt_id)


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
    return await receipt_service.get_by_id(request.receipt_id)

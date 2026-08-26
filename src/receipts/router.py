from typing import Annotated

from fastapi import Depends, Query
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.core.schemes import ErrorResponse
from src.receipts.schemes import FiscalFields, Receipt, ReceiptId
from src.receipts.service import ReceiptsService

router = APIRouter(tags=["Receipts"])


def get_receipts_service(db: AsyncSession = Depends(get_db)):
    return ReceiptsService(db)


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
    "/{receipt_id}",
    response_model=ReceiptId,
    responses={
        404: {"model": ErrorResponse, "description": "Receipt not found"},
    },
)
async def get_receipt_by_id(
    request: Annotated[FiscalFields, Query()],
    receipt_service: ReceiptsService = Depends(get_receipts_service),
) -> Receipt:
    """Returns full recepie info by fiscal data"""
    return await receipt_service.register(request)

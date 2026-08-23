from typing import Annotated

from fastapi import Depends, Path, Query
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.receipts.schemes import (
    ReceiptsCount,
    GetReceiptByIdRequest,
    ReceiptListResponse,
    ReceiptData,
    GetReceiptByFiscalDataRequest,
    TotalSum,
)
from src.core.schemes import ErrorResponse
from src.receipts.service import ReceiptService

router = APIRouter(tags=["API"])


def get_receipt_service(db: AsyncSession = Depends(get_db)):
    return ReceiptService(db)


@router.get("/", include_in_schema=False)
async def root() -> FileResponse:
    """Returns a frontend page with receipt scanner"""
    return FileResponse("static/index.html")


@router.get("/api/receipts/stats/count", response_model=ReceiptsCount)
async def get_receipt_count(
    receipt_service: ReceiptService = Depends(get_receipt_service),
) -> ReceiptsCount:
    """Returns count of receipts in database"""
    return await receipt_service.get_receipt_count()


@router.get("/api/receipts/stats/total-sum", response_model=TotalSum)
async def get_receipt_total_sum(
    receipt_service: ReceiptService = Depends(get_receipt_service),
) -> TotalSum:
    """Returns total sum of all collected receipts"""
    return await receipt_service.get_receipt_total_sum()


@router.get("/api/receipts/export")
async def get_receipts_export(
    receipt_service: ReceiptService = Depends(get_receipt_service),
) -> ReceiptListResponse:
    """Returns full JSON dump of receipts table"""
    return await receipt_service.get_json_dump()


@router.get(
    "/api/receipts/by-fiscal-data",
    response_model=ReceiptData,
    responses={
        404: {"model": ErrorResponse, "description": "Receipt not found"},
        503: {"model": ErrorResponse, "description": "CRPT API not available"},
    },
)
async def get_receipt_by_fiscal_data(
    request: Annotated[GetReceiptByFiscalDataRequest, Query()],
    receipt_service: ReceiptService = Depends(get_receipt_service),
) -> ReceiptData:
    """Returns full recepie info by fiscal data"""
    return await receipt_service.get_receipt_by_fiscal_data(request)


@router.get(
    "/api/receipts/{receipt_id}",
    response_model=ReceiptData,
    responses={
        404: {"model": ErrorResponse, "description": "Receipt not found"},
    },
)
async def get_receipt_by_id(
    request: Annotated[GetReceiptByIdRequest, Path()],
    receipt_service: ReceiptService = Depends(get_receipt_service),
) -> StreamingResponse:
    """Returns receipt by its UUID"""
    return await receipt_service.get_receipt_by_id(request.receipt_id)

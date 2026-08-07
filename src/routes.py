from typing import Annotated

from fastapi import Depends, Path, Query
from fastapi.responses import FileResponse
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.schemes import (
    CountResponse,
    GetReceiptByIdRequest,
    ReceiptResponse,
    GetReceiptByFiscalDataRequest,
)
from src.services import ReceiptService

router = APIRouter(tags=["API"])


def get_receipt_service(db: AsyncSession = Depends(get_db)):
    return ReceiptService(db)


@router.get("/")
async def root() -> FileResponse:
    """Returns a frontend page with receipt scanner"""
    return FileResponse("static/index.html")


@router.get("/api/receipts/count", response_model=CountResponse)
async def count(
    receipt_service: ReceiptService = Depends(get_receipt_service),
) -> CountResponse:
    """Returns count of receipts in database"""
    return await receipt_service.get_receipt_count()


@router.get("/api/receipts/by-fiscal-data", response_model=ReceiptResponse)
async def get_receipt_by_fiscal_data(
    request: Annotated[GetReceiptByFiscalDataRequest, Query()],
    receipt_service: ReceiptService = Depends(get_receipt_service),
) -> ReceiptResponse:
    """Returns full recepie info by fiscal data"""
    return await receipt_service.get_receipt_by_fiscal_data(request)


@router.get("/api/receipts/{receipt_id}")
async def get_receipt_by_id(
    request: Annotated[GetReceiptByIdRequest, Path()],
    receipt_service: ReceiptService = Depends(get_receipt_service),
) -> ReceiptResponse:
    """Returns receipt by its UUID"""
    return await receipt_service.get_receipt_by_id(request.receipt_id)

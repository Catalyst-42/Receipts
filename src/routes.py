from typing import Annotated

from fastapi import Depends, Path, Query
from fastapi.responses import FileResponse
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.schemes import CountResponse, GetReceiptRequest, ReceiptResponse, ScanQRRequest
from src.services import ReceiptService

router = APIRouter()


def get_receipt_service(db: AsyncSession = Depends(get_db)):
    return ReceiptService(db)


@router.get("/")
async def root():
    """Returns a frontend page with receipt scanner"""
    return FileResponse("static/index.html")


@router.post("/api/scan-qr", response_model=ReceiptResponse)
async def scan_qr_code(
    # request: Annotated[ScanQRRequest, Query()],
    request: ScanQRRequest,
    receipt_service: ReceiptService = Depends(get_receipt_service),
):
    """Returns full recepie info by it's QR code"""
    return await receipt_service.scan_qr_code(request.qr_code)


@router.get("/api/receipt/{receipt_id}")
async def get_receipt_by_id(
    request: Annotated[GetReceiptRequest, Path()],
    receipt_service: ReceiptService = Depends(get_receipt_service),
) -> ReceiptResponse:
    """Returns receipt by its UUID"""
    return await receipt_service.get_receipt_by_id(request.receipt_id)


@router.get("/api/count", response_model=CountResponse)
async def count(
    receipt_service: ReceiptService = Depends(get_receipt_service),
) -> CountResponse:
    """Returns count of receipts in database"""
    return await receipt_service.get_receipt_count()

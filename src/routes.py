from fastapi import Depends
from fastapi.responses import FileResponse
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import get_db
from src.schemes import QRCodeRequest, ReceiptResponse
from src.services import ReceiptService

router = APIRouter()


@router.get("/")
async def root():
    """Returns a frontend page with receipt scanner"""
    return FileResponse("static/index.html")


@router.post("/api/scan-qr", response_model=ReceiptResponse)
async def scan_qr_code(request: QRCodeRequest, db: AsyncSession = Depends(get_db)):
    """Returns full recepie info by it's QR code"""
    service = ReceiptService(db)
    return await service.process_qr_code(request.qr_code)

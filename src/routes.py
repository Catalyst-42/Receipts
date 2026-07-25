from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import FileResponse

from src.models import get_db
from src.schemes import QRCodeRequest, ReceiptResponse
from src.services import ReceiptService

router = APIRouter()


@router.get("/")
async def root():
    """Returns frontend page"""
    return FileResponse("static/index.html")


@router.post("/api/scan-qr")
async def scan_qr_code(request: QRCodeRequest, db: AsyncSession = Depends(get_db)):
    """Returns recepie info"""
    service = ReceiptService(db)
    return await service.process_qr_code(request.qr_code)

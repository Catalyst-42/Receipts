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
    ErrorResponse,
)
from src.measures.service import MeasuresService
from src.measures.schemes import Measure, MeasureList

router = APIRouter(prefix="/measures", tags=["Measures"])

def get_measures_service(db: AsyncSession = Depends(get_db)):
    return MeasuresService(db)

@router.get("/", response_model=MeasureList)
async def get_measures(
    service: MeasuresService = Depends(get_measures_service)
) -> MeasureList:
    """Rerutns all directory of item measures"""
    result = await service.get_all()
    return result

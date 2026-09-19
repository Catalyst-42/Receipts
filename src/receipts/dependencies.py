from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.receipts.service import ReceiptsService


def get_receipts_service(db: AsyncSession = Depends(get_db)):
    return ReceiptsService(db)

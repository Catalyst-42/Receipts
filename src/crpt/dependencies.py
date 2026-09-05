from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.crpt.service import CrptService


def get_crpt_service(db: AsyncSession = Depends(get_db)):
    return CrptService(db)

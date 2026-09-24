from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.retailers.service import RetailersService


def get_retailers_service(db: AsyncSession = Depends(get_db)):
    return RetailersService(db)

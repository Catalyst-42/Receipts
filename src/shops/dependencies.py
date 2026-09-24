from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.shops.service import ShopsService


def get_shops_service(db: AsyncSession = Depends(get_db)):
    return ShopsService(db)
